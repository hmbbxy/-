import networkx as nx
import matplotlib.pyplot as plt

def draw_ahp_hierarchy():
    #层次图
    G=nx.DiGraph()
    #添加节点(目标层-准则层-方案层)
    G.add_node('选择最优供应商',layer=0)
    criteria=['质量','成本','效率']
    suppliers=['供应商A','工业商B','供应商C']

    for c in criteria:
        G.add_node(c,layer=1)
        G.add_edge('选择最优供应商',c)

    for s in suppliers:
        G.add_node(s, layer=2)
        for c in criteria:
            G.add_edge(c, s)

# 使用 multipartite_layout 实现分层布局
    pos = nx.multipartite_layout(G, subset_key="layer")
    
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, 
            with_labels=True, 
            node_color=['#FF9999' if G.nodes[n]['layer']==0 
                        else '#99CCFF' if G.nodes[n]['layer']==1 
                        else '#99FF99' for n in G.nodes()],
            node_size=3000,
            font_size=10,
            font_family='SimHei',  # 中文支持
            edge_color='gray',
            arrows=True)
    plt.title("AHP层次结构图", fontsize=14)
    plt.tight_layout()
    plt.show()

draw_ahp_hierarchy()  # 取消注释即可运行