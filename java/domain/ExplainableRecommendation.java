// domain/ExplainableRecommendation.java
public record ExplainableRecommendation(
  String alarmId,
  double sdi,
  double confidence,
  List<String> evidence, // de ex: ["SDI=0.05 <0.80", "2 optiuni deschise", "0 inchise"]
  String explanationAr,
  String explanationFr,
  String explanationEn,
  String auditEventId // append-only
) {}