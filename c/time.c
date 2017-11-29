#include<stdio.h>
#include<time.h>
int main(void)
{
	time_t ca = 0;
	struct tm *time_data;
	const char *days[] = {
		"sunday","monday","tuesday","wednesday","thursday","friday","saturday"
	};
	const char *months[] = {"November"};
	ca = time(NULL);
	printf("\n%s",ctime(&ca));
	time_data = localtime(&ca);
	printf("today is %s %s %d %d\n",
			days[time_data->tm_wday],months[time_data->tm_mon],
			time_data->tm_mday,time_data->tm_year+1900);
	return 0;
}
