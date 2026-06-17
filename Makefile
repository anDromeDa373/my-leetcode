# Root Makefile — project-wide commands
#
# Usage:
#   make ID/FILENAME
#   e.g. make 001/sol1  ->  src/nc001/sol1.cpp

CXX      := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2

ifeq ($(findstring /,$(MAKECMDGOALS)),/)
.PHONY: $(MAKECMDGOALS)
$(MAKECMDGOALS):
	@SPEC='$@'; \
	ID=$${SPEC%%/*}; \
	NAME=$${SPEC#*/}; \
	if [ -z "$$ID" ] || [ -z "$$NAME" ] || [ "$$ID" = "$$NAME" ]; then \
		echo "Error: usage: make ID/FILENAME (e.g. make 001/sol1)"; \
		exit 1; \
	fi; \
	SRC=$$(find src -type f -name "$${NAME}.cpp" -path "*$${ID}*" 2>/dev/null | head -n 1); \
	if [ -z "$$SRC" ]; then \
		echo "Error: File not found: src/*$${ID}*/$${NAME}.cpp"; \
		exit 1; \
	fi; \
	BIN=$$(mktemp /tmp/my-leetcode-run-XXXXXX); \
	echo ">> compiling $$SRC"; \
	if ! $(CXX) $(CXXFLAGS) -o "$$BIN" "$$SRC"; then \
		rm -f "$$BIN"; \
		exit 1; \
	fi; \
	echo ">> running $$BIN"; \
	"$$BIN"; \
	STATUS=$$?; \
	rm -f "$$BIN"; \
	exit $$STATUS
endif
