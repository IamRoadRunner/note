#ifndef _HashQuad_H
typedef unsigned int index;
typedef index position;

struct hashtbl;
typedef struct hashtbl *hashtable;

int NextPrime(int x,int tablesize);
hashtable InitializeTable(int tablesize);
void DestroyTable(hashtable h);
position Find(int key, hashtable h);
void Insert(int key,hashtable h);
int Retrieve(position p,hashtable h);
hashtable Rehash(hashtable h);
#endif 
#define MintableSize 10
enum KindOfEntry{Legitimate, Empty, Deleted};
struct hashentry
{
	int element;
	enum KindOfEntry info;
};

typedef struct hashentry cell;
struct hashtbl
{
	int tablesize;
	cell *thecells;
};
