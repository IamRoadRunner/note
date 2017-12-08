struct Node;
typedef struct Node *ptrtonode;
typedef ptrtonode stack;

int IsEmpty(stack s);
stack CreateStack(void);
void DisposeStack(stack s);
void MakeEmpty(stack s);
void Push (int x, stack s);
int Top(stack s);
void Pop(stack s);

struct Node
{
	int Element;
	ptrtonode Next;
};
