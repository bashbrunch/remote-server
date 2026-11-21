idem=$RANDOM_$RANDOM

expect "GET" "_${idem}/sessions" "" "" "access denied"
expect "POST" "_${idem}/sessions" "" "" "ok"
expect "GET" "_${idem}/sessions" "" "" "ok"

expect_queue $idem "messages" &
expect_queue $idem "proxies" &
expect_queue $idem "prompts" &

wait

expect "POST" "_${idem}/logs" "" "log 1" "ok"
expect "GET" "_${idem}/logs" "" "" "log 1"

expect "POST" "_${idem}/logs" "" "log 2" "ok"
expect "GET" "_${idem}/logs" "" "" "log 1\nlog 2"

expect "DELETE" "_${idem}/sessions" "" "" "ok"

