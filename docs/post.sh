#!/bin/bash

head -n -3 auth.md > auth.mdx; mv auth.mdx auth.md
head -n -3 errors.md > errors.mdx; mv errors.mdx errors.md
head -n -3 pkce.md > pkce.mdx; mv pkce.mdx pkce.md
head -n -3 README.md > README.mdx; mv README.mdx README.md
head -n -3 utils.md > utils.mdx; mv utils.mdx utils.md
