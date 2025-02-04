using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision;
using Microsoft.Azure.CognitiveServices.Vision.ComputerVision.Models;
using Microsoft.Rest.Azure.Authentication;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace OCR.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class OCRController : ControllerBase
    {
        private readonly string endpoint = "https://agileocr.cognitiveservices.azure.com/";
        private readonly string subscriptionKey = "G0IEmnshA6IQxEWeqJhAQEQJ3QbMRb7Of5MiGCmiKS6fP4gV5hZiJQQJ99BBACqBBLyXJ3w3AAAFACOGfuao";

        // POST api/<OCRController>/detect
        [HttpPost("detect")]
        public async Task<IActionResult> OCRDetectAsync([FromBody] OCRRequest request)
        {
            if (string.IsNullOrEmpty(request.BaseImg))
            {
                return BadRequest("Base64 image is empty");
            }

            try
            {
                // Extract Base64 string (handles the possible data URL format)
                string base64Image = ExtractBase64String(request.BaseImg);
                // Initialize Computer Vision Client
                var credentials = new ApiKeyServiceClientCredentials(subscriptionKey);
                var client = new ComputerVisionClient(credentials) { Endpoint = endpoint };

                // Decode base64 string to byte array
                byte[] imageBytes = Convert.FromBase64String(base64Image);
                using (var imageStream = new MemoryStream(imageBytes))
                {
                    // Call the API to read text from the image
                    var recognizeHandwritingResults = await client.ReadInStreamAsync(imageStream);

                    // Get the operation location (URL with the operation ID)
                    string operationLocation = recognizeHandwritingResults.OperationLocation;
                    string operationId = operationLocation.Split('/').Last();

                    // Polling for the operation result
                    ReadOperationResult result = null;
                    while (true)
                    {
                        result = await client.GetReadResultAsync(Guid.Parse(operationId));
                        if (result.Status != OperationStatusCodes.Running && result.Status != OperationStatusCodes.NotStarted)
                        {
                            break;
                        }
                        Thread.Sleep(1000);  // Wait for 1 second before checking again
                    }

                    // Extract the recognized text
                    StringBuilder detectedText = new StringBuilder();

                    if (result.Status == OperationStatusCodes.Succeeded)
                    {
                        foreach (var textResult in result.AnalyzeResult.ReadResults)
                        {
                            foreach (var line in textResult.Lines)
                            {
                                detectedText.AppendLine(line.Text); // Append detected text
                            }
                        }
                    }

                    string finalString = detectedText.ToString();

                  
                    return Ok(new {  detectedText = finalString });

                }

            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        // Method to extract Base64 string from a data URL format
        public string ExtractBase64String(string base64Image)
        {
            if (string.IsNullOrEmpty(base64Image))
                return null;

            // Find the base64 part by splitting at the comma
            var parts = base64Image.Split(',');
            if (parts.Length == 2)
            {
                return parts[1]; // Return only the base64 content
            }

            return base64Image; // If format is incorrect, return as is
        }

        // Method to parse the OCR response and return the text as a string
        public static async Task<string> DetectTextFromBase64Image(string base64String)
        {
            // Initialize Computer Vision Client
            var credentials = new ApiKeyServiceClientCredentials("G0IEmnshA6IQxEWeqJhAQEQJ3QbMRb7Of5MiGCmiKS6fP4gV5hZiJQQJ99BBACqBBLyXJ3w3AAAFACOGfuao");
            var client = new ComputerVisionClient(credentials) { Endpoint = "https://agileocr.cognitiveservices.azure.com/" };

            // Decode base64 string to byte array
            byte[] imageBytes = Convert.FromBase64String(base64String);
            using (var imageStream = new MemoryStream(imageBytes))
            {
                // Call the API to read text from the image
                var recognizeHandwritingResults = await client.ReadInStreamAsync(imageStream);

                // Get the operation location (URL with the operation ID)
                string operationLocation = recognizeHandwritingResults.OperationLocation;
                string operationId = operationLocation.Split('/').Last();

                // Polling for the operation result
                ReadOperationResult result = null;
                while (true)
                {
                    result = await client.GetReadResultAsync(Guid.Parse(operationId));
                    if (result.Status != OperationStatusCodes.Running && result.Status != OperationStatusCodes.NotStarted)
                    {
                        break;
                    }
                    Thread.Sleep(1000);  // Wait for 1 second before checking again
                }

                // Extract the recognized text
                StringBuilder detectedText = new StringBuilder();

                if (result.Status == OperationStatusCodes.Succeeded)
                {
                    foreach (var textResult in result.AnalyzeResult.ReadResults)
                    {
                        foreach (var line in textResult.Lines)
                        {
                            detectedText.AppendLine(line.Text); // Append detected text
                        }
                    }
                }

                return detectedText.ToString();
            }
        }
    }

    public class OCRRequest
    {
        public string BaseImg { get; set; }
    }
}
