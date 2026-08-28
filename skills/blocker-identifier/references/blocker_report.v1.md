# blocker_report.v1

Schema for `/blocker-identifier` output. Manager routing must accept this shape.

## Example

```json
{
  "schema": "blocker_report.v1",
  "slug": "sim_real_comparator",
  "title": "[sim real comparator]",
  "generated_at": "2026-07-23T12:00:00+00:00",
  "pipeline_dir": "C:/Users/avata/aicompete/thepipeline",
  "strike": 2,
  "yield_reviews": 0,
  "status": "budget_exceeded",
  "phase": 3,
  "total_phases": 3,
  "pre_budget_status": "phase_3_validating",
  "budget_lock": false,
  "budget_note": "Force-completed after 59317 min (budget: 135 min for 3-phase project)",
  "blocker_class": "timer_glitch",
  "secondary_classes": ["near_done_unproven", "dep_chain_critical"],
  "near_done": true,
  "timer": {
    "session_started_at": "2026-05-23T13:51:33+00:00",
    "wall_minutes_claimed": 59317,
    "likely_calendar_glitch": true,
    "active_work_minutes_est": null
  },
  "deps_status": [
    {"slug": "video_ingestor_summary", "status": "field_proven", "satisfies": true}
  ],
  "dependents_open": [
    {"title": "sim real discriminator", "requires": ["sim_real_comparator", "video_gan"]}
  ],
  "goal_relevance": "high",
  "goal_ids": [],
  "est_fix_minutes": 45,
  "est_debug_pass_minutes": 30,
  "est_rebuild_minutes": 240,
  "recommended": [
    "AUTO_RETRY_CLEAN",
    "THIN_FIELD",
    "DEBUG_AGAIN",
    "ASK_OPERATOR"
  ],
  "primary_recommendation": "AUTO_RETRY_CLEAN",
  "rationale": "Wall-clock BE after multi-week session stamp; phase 3/3 with workspace artifacts; only open requires blocker for sim_real_discriminator.",
  "next_policy": "remain_queue",
  "ignore_until": null,
  "cooldown_days": null,
  "do_not": [
    "mark_complete_without_proof",
    "soft_satisfy_requires_as_field_proven",
    "spawn_new_ideas_that_re_require_this_slug"
  ],
  "evidence": [
    "pre_budget_status=phase_3_validating",
    "phases/phase_1..3 present",
    "depends_on video_ingestor_summary field_proven"
  ],
  "related_skills": ["systematic-debugging", "field-test"],
  "report_path": "projects/sim_real_comparator/state/blocker_report.json"
}
```

## Field notes

| Field | Required | Notes |
|-------|----------|-------|
| schema | yes | Always `blocker_report.v1` |
| slug | yes | Pipeline project id |
| blocker_class | yes | Primary class |
| recommended | yes | Ordered list from closed menu |
| primary_recommendation | yes | Must be recommended[0] |
| next_policy | yes | remain_queue \| ask_again \| ignore_next \| ignore_until \| cooldown |
| do_not | yes | Guardrails for manager/executor |

## Closed decision menu

`EXTEND_BUDGET` · `DEBUG_AGAIN` · `THIN_FIELD` · `BYPASS_RETURN` · `SOFT_SKIP_REQUIRES` · `SUBSTITUTE` · `IGNORE_NEXT` · `ASK_OPERATOR` · `ARCHIVE_GOAL_EDGE` · `AUTO_RETRY_CLEAN`

## blocker_class enum

`timer_glitch` · `validate_stuck` · `missing_dep` · `scope_too_big` · `wrong_approach` · `external` · `retry_storm` · `near_done_unproven` · `dep_chain_critical` · `missing_project` · `unknown`
