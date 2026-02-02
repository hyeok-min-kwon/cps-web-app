using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using CPSwithML.Models;
using CPSwithML.Services;

namespace CPSwithML.Pages;

public class IndexModel : PageModel
{
    private readonly PredictionService _predictionService;
    private readonly ILogger<IndexModel> _logger;

    [BindProperty]
    public SensorDataDto SensorData { get; set; } = new SensorDataDto();

    public PredictionResultDto? PredictionResult { get; set; }
    public string? ErrorMessage { get; set; }

    public IndexModel(PredictionService predictionService, ILogger<IndexModel> logger)
    {
        _predictionService = predictionService;
        _logger = logger;
    }

    public void OnGet()
    {
        // 기본값 설정 --> 접속 기본
        SensorData = new SensorDataDto
        {
            Type = "L",
            AirTemperature = 298.0,
            ProcessTemperature = 308.0,
            RotationalSpeed = 1500,
            Torque = 40.0,
            ToolWear = 0
        };
    }
    // 예측 요청 처리
    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            return Page();
        }

        try
        {
            _logger.LogInformation("예측 요청: {@SensorData}", SensorData);

            // Python API 호출하여 예측 수행
            PredictionResult = await _predictionService.PredictFailureAsync(SensorData);

            if (PredictionResult == null)
            {
                ErrorMessage = "예측 결과를 받을 수 없습니다. Python API 서버를 확인하세요.";
                return Page();
            }

            _logger.LogInformation("예측 성공: {@PredictionResult}", PredictionResult);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "예측 중 오류 발생");
            ErrorMessage = ex.Message;
        }

        return Page();
    }
}
