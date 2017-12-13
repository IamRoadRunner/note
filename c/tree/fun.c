void printtree(searchtree t)
{
	if(t!=NULL)
	{
		printtree(t->left);
		printelement(t->element);
		printtree(t->right);
	}
}

int height(tree t)
{
	if(t==NULL)
		return -1;
	else
		return ++max(height(t->left),height(t->right));
}
