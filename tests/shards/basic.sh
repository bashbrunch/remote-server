idem=$RANDOM_$RANDOM

expect "POST" "_${idem}_1/sessions" "" "" "ok"
expect "POST" "_${idem}_2/sessions" "" "pwd" "ok"
expect "POST" "_${idem}_2/sessions" "" "pwd" "access denied"
expect "POST" "_${idem}_2/sessions" "pwd" "password" "ok"

expect "DELETE" "_${idem}_1/sessions" "" "" "ok"
expect "DELETE" "_${idem}_1/sessions" "" "" "access denied"
expect "DELETE" "_${idem}_2/sessions" "pwd" "" "access denied"
expect "DELETE" "_${idem}_2/sessions" "password" "" "ok"

