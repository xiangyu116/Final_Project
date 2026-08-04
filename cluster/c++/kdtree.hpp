#ifndef KDTREE_HPP
#define KDTREE_HPP

#include <vector>
#include <algorithm>
#include <cmath>

using Point = std::vector<double>;

class KDTree
{
private:

    struct Node
    {
        int index;
        int axis;
        Node* left;
        Node* right;

        Node(int i,int a)
        {
            index=i;
            axis=a;
            left=nullptr;
            right=nullptr;
        }
    };


    const std::vector<Point>& data;
    Node* root;
    int dimensions;


    Node* build(std::vector<int>& ids,int depth)
    {
        if(ids.empty())
        {
            return nullptr;
        }
        int axis=depth%dimensions;

        std::sort(ids.begin(),ids.end(),
            [&](int a,int b)
            {
                return data[a][axis]<data[b][axis];
            }
        );

        int mid=ids.size()/2;

        Node* node=new Node(ids[mid],axis);

        std::vector<int> left(ids.begin(), ids.begin()+mid);
        std::vector<int> right(ids.begin()+mid+1,ids.end());

        node->left=build(left,depth+1);
        node->right=build(right,depth+1);

        return node;
    }



    void radiusSearch(Node* node,const Point& target,double eps2,std::vector<int>& result)
    {
        if(node==nullptr)
        {
            return;
        }

        double distance=0.0;

        for(int i=0;i<dimensions;i++)
        {
            double diff=
            target[i]-data[node->index][i];

            distance+=diff*diff;
        }

        if(distance<=eps2)
        {
            result.push_back(node->index);
        }

        double diff=target[node->axis]-data[node->index][node->axis];

        if(diff<=0)
        {
            radiusSearch(node->left,target,eps2,result);

            if(diff*diff<=eps2)
            {
                radiusSearch(node->right,target,eps2,result);
            }
        }
        else
        {
            radiusSearch(node->right, target,eps2,result);

            if(diff*diff<=eps2)
            {
                radiusSearch(node->left,target, eps2,result);
            }
        }

    }


public:

    KDTree(const std::vector<Point>& points)
      :data(points)
    {
        dimensions=points[0].size();

        std::vector<int> ids(points.size());
        for(int i=0;i<points.size();i++)
        {
            ids[i]=i;
        }

        root=build(ids,0);
    }


    std::vector<int> radiusSearch(const Point& target,double eps)
    {
        std::vector<int> result;
        radiusSearch(root,target,eps*eps,result);
        return result;
    }

};


#endif