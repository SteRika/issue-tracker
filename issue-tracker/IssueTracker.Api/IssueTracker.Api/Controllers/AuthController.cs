using Microsoft.AspNetCore.Mvc;
using IssueTracker.Api.Models;
using IssueTracker.Api.Helpers;
using System.IdentityModel.Tokens.Jwt;

namespace api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly IConfiguration _config;

        // Example static users (in real app, use DB)
        private static List<User> Users = new List<User>
        {
            new User { Username = "admin", Password = "admin123", Role = "Admin" },
            new User { Username = "user", Password = "user123", Role = "User" }
        };

        public AuthController(IConfiguration config)
        {
            _config = config;
        }

        [HttpPost("login")]
        public IActionResult Login([FromBody] LoginDto dto)
        {
            var user = Users.SingleOrDefault(u => u.Username == dto.Username && u.Password == dto.Password);
            if (user == null)
                return Unauthorized("Invalid username or password");

            var token = JwtHelper.GenerateJwtToken(user, _config["Jwt:Key"]);
            return Ok(new { token, role = user.Role });
        }
    }
}