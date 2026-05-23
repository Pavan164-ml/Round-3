"""
DAY 4 — BEHAVIORAL QUESTIONS & STAR STORIES (LIGHT DAY)
Interview: 26 May 2026

Complete all stories with Situation → Task → Action → Result format.
Quantify results whenever possible.
"""

# =============================================================================
# STORY 1: Large-Scale Pipeline [✅ Ready]
# =============================================================================

"""
Q: Tell me about a large-scale data pipeline you built.

SITUATION:
  The company needed to process customer interaction data from 100+ countries 
  daily to power targeted advertising campaigns. The data was massive (100+ TB/day),
  and the existing pipeline couldn't scale.

TASK:
  Design and optimize a PySpark ETL pipeline on AWS EMR, orchestrated via Airflow,
  that could reliably process 100+ TB of data daily with cost efficiency.

ACTION:
  - Built a partitioned Parquet pipeline using PySpark on EMR, partitioning by date and country
  - Tuned Spark config for performance: enabled AQE, used broadcast joins for dimension tables,
    set appropriate shuffle partitions (2-3x cores)
  - Implemented automated monitoring via Airflow DAGs with SLA miss callbacks
  - Task nodes on Spot instances (60% cost reduction) with fallback to on-demand
  - Added quality validation layer with Great Expectations between Silver/Gold

RESULT:
  - 100+ TB processed reliably every day within the SLA window
  - Enabled 200M+ annual revenue campaigns through better targeting
  - 10% quarterly increase in targeting rate
  - 60% cost reduction via Spot instances + optimized Spark config
"""


# =============================================================================
# STORY 2: Improved Observability [✅ Ready]
# =============================================================================

"""
Q: Describe a time you improved system observability or caught a data quality issue.

SITUATION:
  Downstream business teams were discovering data quality issues only after reports
  were wrong — hours or days after the data was consumed. By then, decisions had 
  already been made based on bad data.

TASK:
  Implement proactive anomaly detection across 8 critical data tables so that issues
  were caught before they reached business dashboards.

ACTION:
  - Built monitoring using Databricks Lakehouse Monitoring 
  - Compared metrics (row count, null percentage, distribution shifts) to historical 
    30-day averages with configurable threshold multipliers (e.g., alert if row_count 
    drops >20% from avg)
  - Configured automated alerts via webhooks to Slack/email
  - Set up snapshot profiling for daily comparison and timeseries monitoring for trends
  - Documented runbooks for each type of alert with remediation steps

RESULT:
  - Early detection of data issues before they impacted business decisions
  - Stakeholders now receive alerts within minutes of anomaly occurrence
  - Reduced mean-time-to-detection from hours to minutes
"""


# =============================================================================
# STORY 3: GenAI / LLMs in Production [✅ Ready]
# =============================================================================

"""
Q: Have you worked with GenAI / LLMs in a production context?

SITUATION:
  The data catalog had thousands of undocumented columns across dozens of tables.
  Analysts spent ~2 hours per table manually documenting column descriptions, 
  slowing their productivity significantly.

TASK:
  Onboard 10+ tables to an LLM-powered column description generator that auto-generated
  descriptions from existing documentation, wikis, and code repositories.

ACTION:
  - Extended the existing RAG pipeline architecture: indexed wikis, Git repos, and 
    knowledge transfer transcripts into a vector database (Pinecone)
  - For each table, retrieved relevant documentation chunks and sent to LLM with 
    a structured prompt to generate column-level descriptions in JSON format
  - Updated DDLs with generated descriptions and debugged pipeline failures 
    (schema changes, missing chunks, LLM hallucination)
  - Used system prompting + few-shot examples to ensure consistent output format
  - Built feedback loop: allowed analysts to accept/edit/reject generated descriptions

RESULT:
  - 10+ tables documented automatically, saving ~2 hours of manual documentation per table
  - Descriptions were grounded in existing documentation (RAG reduced hallucination)
  - Pipeline scaled easily to more tables without proportional increase in effort
"""


# =============================================================================
# STORY 4: Reduced Operational Toil [✅ Ready]
# =============================================================================

"""
Q: Tell me about a time you reduced operational toil through automation.

SITUATION:
  Engineers were spending ~2 hours every day manually checking Airflow DAG statuses 
  across all pipelines. This was tedious, error-prone, and delayed issue detection.

TASK:
  Automate the monitoring and alerting process so engineers could focus on 
  improvements instead of manual checks.

ACTION:
  - Configured an automated Airflow DAG that ran every 3 hours 
  - Aggregated pipeline statuses (success/failed/running) across all production DAGs
  - Generated consolidated reports with pass/fail summaries, execution times, and trends
  - Integrated with Slack webhook to send reports automatically
  - Added SLA miss callbacks for early warning of pipeline delays
  - Implemented a "pipeline health score" metric (successful_runs / total_runs)

RESULT:
  - 2 hours/day of manual monitoring completely eliminated
  - Proactive issue resolution: team knows about failures within 3 hours instead of 
    discovering them during morning manual check
  - Pipeline health score provided objective measure of platform reliability
"""


# =============================================================================
# STORY 5: Cross-functional Collaboration [✅ Ready]
# =============================================================================

"""
Q: Describe a time you worked cross-functionally to deliver a technical solution.

SITUATION:
  The business team needed finer-grained targeting capabilities (machine-level targeting), 
  but the existing data model only had customer-level attributes. They lacked the data 
  granularity to execute this new strategy.

TASK:
  Translate business targeting requirements into pipeline enhancements — extend the 
  data model to support machine-level attributes and update all downstream pipelines.

ACTION:
  - Collaborated intensively with product and business teams to understand their 
    targeting needs and data requirements
  - Extended the data model with new machine-level attributes (machine ID, type, 
    location, install base, usage metrics)
  - Updated upstream ingestion pipelines to capture the new attributes
  - Modified downstream aggregation jobs to include machine-level dimensions
  - Coordinated testing with QA and business teams to validate the new attributes
  - Documented the new data model and communicated changes to all stakeholders

RESULT:
  - Machine-level targeting enabled across all customer segments
  - 10% per quarter increase in targeting rate as campaigns became more precise
  - Stronger cross-functional relationships: business team understood data constraints;
    data team understood business priorities
"""


# =============================================================================
# STORY 6: Technical Challenge Under Pressure [📌 Draft → ✅ Ready]
# =============================================================================

"""
Q: Tell me about a technical challenge you solved under pressure.

SITUATION:
  A critical production pipeline was failing intermittently during the peak 
  processing window. The 100TB/day ETL job would crash about 30 minutes into 
  execution, causing downstream reports to be delayed by 4+ hours. The issue 
  happened at 2 AM on a Saturday.

TASK:
  Diagnose and fix the pipeline failure ASAP to restore the daily data delivery 
  SLA. The business was unable to run Sunday morning campaigns without this data.

ACTION:
  - SSH'd into EMR cluster immediately and checked the Spark UI logs at the 
    stage that was consistently failing (Stage 42 — the large sort-merge join)
  - Identified that one partition had 80% of the data due to a skewed join key: 
    a major customer event had 10× normal volume that day
  - Applied emergency fix: broadcast-hinted the smaller dimension table (normally 
    this wasn't small enough, but after checking, it was 8MB < 10MB threshold)
  - For permanent fix the next day: enabled AQE skew join handling and added 
    salting logic to redistribute skewed keys
  - Ran the pipeline manually with the fix and monitored through to completion

RESULT:
  - Pipeline completed successfully within 45 minutes of starting the fix
  - Downstream reports delivered on time; Sunday campaigns ran as scheduled
  - Permanent fix (AQE skew join + salting) prevented recurrence
  - Documented the incident response in a runbook for future on-call engineers
"""


# =============================================================================
# STORY 7: 3-Year Technical Vision [📌 Draft → ✅ Ready]
# =============================================================================

"""
Q: Where do you see yourself in 3 years technically?

"Three years from now, I see myself as a Lead/Senior Data Platform Engineer who 
effectively bridges the gap between traditional Data Engineering and AI/ML 
infrastructure. Specifically:

1. ARCHITECTURE: I want to be designing production-grade GenAI data pipelines — 
   systems that reliably ingest, process, and serve data for RAG applications, 
   model training, and real-time ML inference at scale.

2. PLATFORM THINKING: I want to move beyond building individual pipelines to 
   designing data platforms where data scientists, analysts, and app engineers 
   can self-serve their data needs without bottlenecks.

3. MENTORSHIP: I want to be the person junior engineers come to for guidance on 
   Spark optimization, pipeline design patterns, and AI system architecture. 
   I find teaching reinforces my own understanding.

4. EMERGING TECH: I'm actively investing in learning GenAI infrastructure 
   (vector databases, LLM serving, RAG patterns) because I believe the next 
   3 years will see 'Data Engineering + AI' become the default expectation, 
   not a specialization.

I want to be deep enough in both Data Engineering fundamentals and GenAI 
systems to architect end-to-end solutions — from data ingestion to LLM 
deployment — with production reliability."


**Why this is a strong answer:**
- Shows ambition to grow but stays technically focused (not "I want to be a manager")
- Connects current experience to future trends (Data Engineering → AI)
- Demonstrates mentorship interest (team player)
- Mentions specific technologies (shows genuine depth, not generic statements)
"""


# =============================================================================
# STORY 8: Why This Company / Role [📌 Draft → ✅ Ready]
# =============================================================================

"""
Q: Why this company / this role?

For each interview, customize these points:

1. ALIGNMENT WITH MISSION:
   "I'm excited by [Company Name]'s mission to [specific mission]. As a data 
   engineer, I've seen how quality data infrastructure directly enables better 
   business decisions and customer experiences, and I want to contribute to 
   [Company]'s impact in [specific domain]."

2. TECHNICAL EXCITEMENT:
   "I'm particularly drawn to [Company's specific challenge]. My experience 
   building [your large pipeline/GenAI app] directly translates to the type of 
   work being done here, and I see opportunities to [specific contribution]."

3. SCALE CHALLENGE:
   "[Company] operates at [specific scale] which is exactly the type of 
   challenge I thrive on. I enjoy the complexity that comes with scale — 
   optimizing Spark jobs, managing data quality, designing reliable pipelines."

4. GROWTH & CULTURE:
   "I value [Company's approach to engineering or culture aspect]. The 
   opportunity to work alongside [specific teams or tech stack] aligns with 
   where I want to grow technically."


**Generic template (fill in company details):**
"I've been following [Company]'s work in [domain], and I'm impressed by how 
you've [specific achievement]. My experience building a 100TB/day pipeline and 
a GenAI metadata application directly aligns with your need for engineers who 
can handle both traditional data infrastructure and emerging AI workloads. 
I'm looking for a role where I can architect systems at scale while growing 
into GenAI infrastructure, and [Company]'s [specific product/project] is 
exactly that intersection. I also value [specific company culture point], 
which aligns with how I work best."
"""


# =============================================================================
# STAR STORY DELIVERY TIPS
# =============================================================================

"""
STRUCTURE:
  S: 2-3 sentences setting context
  T: 1-2 sentences defining the specific challenge
  A: 4-5 sentences — this is THE MOST IMPORTANT part. Be detailed about WHAT you did.
  R: 1-2 sentences with QUANTIFIED impact

DELIVERY TIPS:
  - Rehearse out loud — stories should feel natural, not scripted
  - Keep each story to 60-90 seconds
  - Lead with: "Let me tell you about [story theme]..."
  - Quantify everything: instead of "improved performance" → "reduced processing time by 60%"
  - Use technical language naturally: "I tuned AQE, enabled broadcast joins, and implemented salting"
  - If the interviewer asks a clarifying question, dive deeper — that's a good sign
  - Have 5 stories ready; you'll likely only use 2-3

COMMON PITFALLS:
  ✗ Being too vague: "I fixed the pipeline" — what was wrong? What exactly did you do?
  ✗ No quantification: "It was faster" — how much faster? What was the business impact?
  ✗ Rambling: Practice to keep each story tight and focused
  ✓ Using "we" appropriately — acknowledge team, but highlight YOUR specific contribution
"""

print("=== END OF DAY 4 — BEHAVIORAL + STAR STORIES ===")
print("All 8 STAR stories ready for the interview!")