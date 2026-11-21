TESTS=$(dirname "$0")

source "$TESTS/core/setup.sh"
source "$TESTS/core/analytics.sh"
source "$TESTS/core/macros.sh"

test_start_time=$(date +%s%N)

for shard in $(ls "$TESTS/shards" | grep -E ".*\.sh$"); do
  source "$TESTS/shards/${shard}" &
done

wait

test_end_time=$(date +%s%N)
test_duration_ns=$((test_end_time - test_start_time))
test_duration_ms=$((test_duration_ns / 1000000))

printf "Total time: ${test_duration_ms} ms\n\n"

