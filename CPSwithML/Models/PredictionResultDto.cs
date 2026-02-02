using System.Text.Json.Serialization;

namespace CPSwithML.Models;

public class PredictionResultDto
{
    [JsonPropertyName("machine_failure")]
    public MachineFailurePrediction MachineFailure { get; set; } = null!;

    [JsonPropertyName("failure_types")]
    public Dictionary<string, double> FailureTypes { get; set; } = new();
}

public class MachineFailurePrediction
{
    [JsonPropertyName("prediction")]
    public int Prediction { get; set; }

    [JsonPropertyName("probability")]
    public double Probability { get; set; }
}
