#ifdef _Queue_h
struct queryrecord;
typedef struct queuerecord *queue;

int IsEmpty(queue q);
int IsFull(queue q);
queue CreateQueue(int maxelements);
void DisposeQueue(queue q);
void MakeEmpty(queue q);
void Enqueue(int x, queue q);
int Front(queue q);
void Dequeue(queue q);
int FrontAndDequeue(queue q);
#endif

#define MinQueueSize(5)

struct queuerecord
{
	int capacity;
	int front;
	int rear;
	int size;
	int *array;
};
