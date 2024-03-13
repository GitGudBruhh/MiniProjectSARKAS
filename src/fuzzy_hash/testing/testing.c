#include<stdio.h>
#include<fuzzy.h>

int main {
	char* buf = "abcdefg";
	int buf_len = 8;
	char* result = malloc(FUZZY_MAX_RESULT);

	fuzzy_hash_buf(buf, buf_len, result);
	return 0;
}

