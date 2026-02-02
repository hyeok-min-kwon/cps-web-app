using System.Text;
using System.Text.Json;
using CPSwithML.Models;

namespace CPSwithML.Services;

public class PredictionService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PredictionService> _logger;
    private readonly string _apiBaseUrl;

    public PredictionService(HttpClient httpClient, ILogger<PredictionService> logger, IConfiguration configuration)
    {
        _httpClient = httpClient;
        _logger = logger;
        _apiBaseUrl = configuration["PredictionApi:BaseUrl"] ?? "http://localhost:8000";
    }

    // 기계 고장 예측
    public async Task<PredictionResultDto?> PredictFailureAsync(SensorDataDto sensorData)
    {
        try
        {
            _logger.LogInformation("예측 요청 시작: Type={Type}, AirTemp={AirTemp}",
                sensorData.Type, sensorData.AirTemperature);

            var json = JsonSerializer.Serialize(sensorData, new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
            });

            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_apiBaseUrl}/predict", content);

            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                _logger.LogError("API 호출 실패: StatusCode={StatusCode}, Error={Error}",
                    response.StatusCode, errorContent);
                return null;
            }

            var responseJson = await response.Content.ReadAsStringAsync();
            _logger.LogInformation("API 응답: {Response}", responseJson);

            var result = JsonSerializer.Deserialize<PredictionResultDto>(responseJson,
                new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

            _logger.LogInformation("예측 완료: Failure={Failure}, Probability={Probability}",
                result?.MachineFailure.Prediction, result?.MachineFailure.Probability);

            return result;
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(ex, "Python API 서버에 연결할 수 없습니다. API 서버가 실행 중인지 확인하세요.");
            throw new Exception("예측 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.", ex);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "예측 중 오류 발생");
            throw new Exception("예측 중 오류가 발생했습니다.", ex);
        }
    }
    // API 상태 확인
    public async Task<bool> CheckApiHealthAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_apiBaseUrl}/health");
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }
}
