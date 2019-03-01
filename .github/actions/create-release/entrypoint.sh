#!/usr/bin/env bash
VERSION="${GITHUB_REF/refs\/tags\/v/}"

# awk code to get description of the release from CHANGELOG.rst.
# Assumes that the changelog uses captions with the exact version
# number and a ~ type header (i.e. underline with ~ after the line
# with the version number)
GET_DESCRIPTION_AWK_CODE=$(cat <<EOF
BEGIN {do_print=0}
{
    if (\$0 == "${VERSION}") {
        do_print=1;
    } else {
        if (do_print && \$0 != "" && \$0 !~ /~+/) {
            if (\$0 ~ /[~\\- ].*/) {
                printf "%s\\\\n",\$0;
            } else {
                exit;
            }
        }
    }
}
EOF
           )

DESCRIPTION=$(awk "${GET_DESCRIPTION_AWK_CODE}" CHANGELOG.rst)

JSON=$(cat <<EOF
{
  "tag_name": "v${VERSION}",
  "target_commitish": "master",
  "name": "${VERSION}",
  "body": "${DESCRIPTION}",
  "draft": false,
  "prerelease": false
}
EOF
    )

AUTH_HEADER="Authorization: token ${GITHUB_TOKEN}"
URL="https://api.github.com/repos/${GITHUB_REPOSITORY}/releases"

curl \
    -sSL \
    --fail \
    -XPOST \
    -H "${AUTH_HEADER}" \
    --header "Content-Type: application/json" \
    --data "${JSON}" \
    "${URL}"
