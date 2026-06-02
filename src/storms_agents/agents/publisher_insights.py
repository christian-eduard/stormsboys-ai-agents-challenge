from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import BookAnalysis, PublisherInsight, PublisherReport


class PublisherInsightsAgent:
    name = "PublisherInsightsAgent"

    def run(
        self,
        analysis: BookAnalysis,
        evaluation_summary: dict[str, object],
    ) -> AgentResult[PublisherReport]:
        with trace_span(self.name, "publisher.generate_insights") as trace:
            total_cases = int(evaluation_summary.get("totalCases", 0))
            optimized_passed = int(evaluation_summary.get("optimizedPassed", 0))
            quality_score = optimized_passed / total_cases if total_cases else 0.0
            engagement_score = min(
                1.0,
                (len(analysis.characters) * 0.18)
                + (len(analysis.scenes) * 0.12)
                + (len(analysis.places) * 0.06),
            )
            report = PublisherReport(
                audience="publishers, authors, education platforms, and premium reading apps",
                business_value=(
                    "Turns a book catalog into interactive, measurable reader experiences "
                    "without rebuilding each title as a bespoke app."
                ),
                engagement_score=round(engagement_score, 2),
                quality_score=round(quality_score, 2),
                insights=[
                    PublisherInsight(
                        metric="Character engagement",
                        value=f"{len(analysis.characters)} interactive character agents",
                        recommendation=(
                            "Use character-level conversations as premium reader engagement."
                        ),
                    ),
                    PublisherInsight(
                        metric="Narrative coverage",
                        value=(
                            f"{len(analysis.scenes)} key scenes and "
                            f"{len(analysis.places)} places mapped"
                        ),
                        recommendation=(
                            "Prioritize scene prompts for classroom and book club use cases."
                        ),
                    ),
                    PublisherInsight(
                        metric="Agent reliability",
                        value=f"{optimized_passed}/{total_cases} optimized evaluation cases passed",
                        recommendation=(
                            "Expose traces and consistency checks as publisher trust signals."
                        ),
                    ),
                ],
            )
            trace.input_tokens = len(analysis.summary.split()) + total_cases
            trace.output_tokens = len(report.insights)
            return AgentResult(output=report, traces=[trace])
