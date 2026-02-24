# Quickstart Tests

## Mastery Calc
curl -X POST dapr invoke --app-id progress-service --method post --data '{"event_type":"exercise.completed","student_id":"test","score":80}'

Verify state: dapr state get --state-store statestore --key test-student

## Struggle Alert
Simulate 3 failures: publish to exercise.failed x3 same topic

Check /struggles returns alert
