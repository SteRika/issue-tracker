using IssueTracker.Api.Data;
using IssueTracker.Api.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(o =>
    o.UseSqlite(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// HttpClient for AI service
builder.Services.AddHttpClient("Ai", client =>
{
    var baseUrl = builder.Configuration["AiService:BaseUrl"] ?? "http://localhost:8000";
    client.BaseAddress = new Uri(baseUrl);
});

// Add services
builder.Services.AddControllers();
builder.Services.AddAuthentication("Bearer")
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.ASCII.GetBytes(builder.Configuration["Jwt:Key"])),
            ValidateIssuer = false,
            ValidateAudience = false
        };
    });

builder.Services.AddAuthorization();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.MapGet("/", () => Results.Redirect("/swagger"));
app.UseAuthentication();
app.UseAuthorization();

var api = app.MapGroup("/api");

// CRUD: Issues
api.MapGet("/issues", async (AppDbContext db) => await db.Issues.OrderByDescending(i => i.Id).ToListAsync());

api.MapGet("/issues/{id:int}", async (int id, AppDbContext db) =>
    await db.Issues.FindAsync(id) is { } issue ? Results.Ok(issue) : Results.NotFound());

api.MapPost("/issues", async (Issue input, AppDbContext db) =>
{
    db.Issues.Add(input);
    await db.SaveChangesAsync();
    return Results.Created($"/api/issues/{input.Id}", input);
});

api.MapPut("/issues/{id:int}", async (int id, Issue update, AppDbContext db) =>
{
    var issue = await db.Issues.FindAsync(id);
    if (issue is null) return Results.NotFound();

    issue.Title = update.Title;
    issue.Description = update.Description;
    issue.Status = update.Status;
    issue.Priority = update.Priority;
    await db.SaveChangesAsync();
    return Results.NoContent();
});

api.MapDelete("/issues/{id:int}", async (int id, AppDbContext db) =>
{
    var issue = await db.Issues.FindAsync(id);
    if (issue is null) return Results.NotFound();
    db.Remove(issue);
    await db.SaveChangesAsync();
    return Results.NoContent();
});

// Integrate with AI: classify an issue's priority by title+description
api.MapPost("/issues/{id:int}/classify", async (int id, AppDbContext db, IHttpClientFactory http) =>
{
    var issue = await db.Issues.FindAsync(id);
    if (issue is null) return Results.NotFound();

    var client = http.CreateClient("Ai");
    var payload = new { title = issue.Title, description = issue.Description };
    var res = await client.PostAsJsonAsync("/predict", payload);
    if (!res.IsSuccessStatusCode) return Results.Problem("AI service unavailable", statusCode: 503);

    var data = await res.Content.ReadFromJsonAsync<PriorityResponse>();
    if (data is null) return Results.Problem("AI response invalid", statusCode: 502);

    issue.Priority = data.priority;
    await db.SaveChangesAsync();

    return Results.Ok(new { issue.Id, issue.Title, issue.Priority });
});
app.MapControllers();
app.Run();

record PriorityResponse(string priority);