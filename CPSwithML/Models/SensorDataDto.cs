using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace CPSwithML.Models;

/// 센서 데이터 전송용 DTO
public class SensorDataDto
{
    [Required]
    [RegularExpression("^[LMH]$", ErrorMessage = "Type은 L, M, H 중 하나여야 합니다.")]
    [JsonPropertyName("type")]
    public string Type { get; set; } = "M";

    [Required]
    [Range(290, 310, ErrorMessage = "공기 온도는 290K에서 310K 사이여야 합니다.")]
    [JsonPropertyName("air_temperature")]
    public double AirTemperature { get; set; } = 298.0;

    [Required]
    [Range(300, 315, ErrorMessage = "공정 온도는 300K에서 315K 사이여야 합니다.")]
    [JsonPropertyName("process_temperature")]
    public double ProcessTemperature { get; set; } = 308.0;

    [Required]
    [Range(1000, 3000, ErrorMessage = "회전 속도는 1000rpm에서 3000rpm 사이여야 합니다.")]
    [JsonPropertyName("rotational_speed")]
    public int RotationalSpeed { get; set; } = 1500;

    [Required]
    [Range(0, 100, ErrorMessage = "토크는 0Nm에서 100Nm 사이여야 합니다.")]
    [JsonPropertyName("torque")]
    public double Torque { get; set; } = 40.0;

    [Required]
    [Range(0, 300, ErrorMessage = "공구 마모는 0분에서 300분 사이여야 합니다.")]
    [JsonPropertyName("tool_wear")]
    public int ToolWear { get; set; } = 0;
}
