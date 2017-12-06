#include<stdio.h>
#include<math.h>
typedef struct
{
	int coeffarray[maxdegree+1];
	int highpower;
}*polynomail;

int max(int x, int y)
{
	return x>y?x:y;
}

void zeropolynomail(polynomail poly)
{
	int i;
	for(i=0;i<poly->maxdegree;i++)
		poly->highpower=0;
}

void addpolynomail(const polynomail poly1,
		const polynomail poly2, polynomail polysum)
{
	int i;
	zeropolynomail(polysum);
	polysum->highpower=max(poly1->highpower,poly2->highpower);
	for (i=polysum->highpower; i>=0;i--)
		polysum->coeffarray[i]=poly1->coeffarray[i]+poly2->coeffarray[i];
}
void multpolynomail(const polynomail poly1,
		const polynomail poly2, polynomail polyprod)
{
	int i,j;
	zeropolynomail(polyprod);
	polyprod->highpower=poly1->highpower+poly2->highpower;
	if(polyprod->highpower > maxdegree )
		printf("超过数组长度");
	else
		for (i=0;i<=poly1->highpower;i++)
			for(j=0;j<=poly2->highpower;j++)
				polyprod->coeffarray[i+j]+=poly1->coeffarray[i]*poly2->coeffarray[j];
}

int main(void)
{

}
