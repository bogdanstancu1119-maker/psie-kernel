// api/IntelligenceController.java
@RestController
@RequestMapping("/api/v1/intelligence")
public class IntelligenceController {
  @PostMapping("/explain")
  public ExplainableRecommendation explain(@RequestBody AlarmExplainRequest req){
    // Nu scrie direct in telemetry - cheama portul din monitoring
    return intelligenceAppService.explainWithSDI(req);
  }
}