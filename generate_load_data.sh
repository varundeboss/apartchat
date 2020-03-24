python3 generate_data.py

#/opt/couchbase/bin/couchbase-cli bucket-flush -c couchbase://127.0.0.1 -u admin -p vArundebo0s --bucket=vc-search

/opt/couchbase/bin/cbimport json -c couchbase://127.0.0.1 -u admin -p vArundebo0s -b vc-search -d file:///home/varun/workspace/personal/programs/posts -f lines -g %type%::%id%
/opt/couchbase/bin/cbimport json -c couchbase://127.0.0.1 -u admin -p vArundebo0s -b vc-search -d file:///home/varun/workspace/personal/programs/users -f lines -g %type%::%id%
/opt/couchbase/bin/cbimport json -c couchbase://127.0.0.1 -u admin -p vArundebo0s -b vc-search -d file:///home/varun/workspace/personal/programs/apartments -f lines -g %type%::%id%
