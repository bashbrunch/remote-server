idem=$RANDOM_$RANDOM

expect "GET" "_${idem}/sessions" "" "" "access denied"
expect "POST" "_${idem}/sessions" "" "" "ok"
expect "GET" "_${idem}/sessions" "" "" "ok"

expect_queue $idem "logs" &
expect_queue $idem "messages" &
expect_queue $idem "proxies" &
expect_queue $idem "prompts" &

wait

expect "DELETE" "_${idem}/sessions" "" "" "ok"

