import numpy as np

def ahp_geometric_method(matrix):
    """方根法(几何平均法)计算AHP权重"""
    n = matrix.shape[0]
    # 1. 计算每行几何平均
    row_geometric_mean = np.prod(matrix, axis=1) ** (1/n)
    # 2. 归一化得到权重
    weights = row_geometric_mean / np.sum(row_geometric_mean)
    return weights

def ahp_sum_product_method(matrix):
    """和积法计算AHP权重"""
    n = matrix.shape[0]
    # 1. 按列归一化
    col_sum = np.sum(matrix, axis=0)
    normalized_matrix = matrix / col_sum
    # 2. 按行求和
    row_sum = np.sum(normalized_matrix, axis=1)
    # 3. 再次归一化
    weights = row_sum / np.sum(row_sum)
    return weights

def consistency_check(matrix, weights):
    """一致性检验"""
    n = matrix.shape[0]
    # 计算最大特征值 lambda_max
    # 对于方根法，lambda_max ≈ sum((A*w)_i / w_i) / n
    Aw = np.dot(matrix, weights)
    lambda_max = np.mean(Aw / weights)
    
    CI = (lambda_max - n) / (n - 1)
    
    # 平均随机一致性指标 RI (1-10阶)
    RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 
               6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    RI = RI_dict.get(n, 1.49) # 若n>10，用1.49近似
    
    CR = CI / RI if RI != 0 else 0
    return CR

# 准则层判断矩阵 (质量 vs 成本 vs 效率)
# 假设: 质量比成本稍重要(3), 质量比效率明显重要(5), 成本比效率稍重要(2)
A_criteria = np.array([
    [1,   3,   5],
    [1/3, 1,   2],
    [1/5, 1/2, 1]
])

print("=== 准则层权重计算 ===")
w_criteria_geo = ahp_geometric_method(A_criteria)
w_criteria_sum = ahp_sum_product_method(A_criteria)

print(f"方根法(几何平均)权重: {w_criteria_geo}")
print(f"和积法权重: {w_criteria_sum}")

CR = consistency_check(A_criteria, w_criteria_geo)
print(f"一致性比率 CR = {CR:.4f} {'✅ 通过' if CR < 0.1 else '❌ 未通过'}")

# 假设方案层对准则的权重已知（此处省略计算过程）
# 方案层权重 (供应商A, B, C) 对各个准则
# 例如：对质量准则的方案权重
w_suppliers_quality = np.array([0.6, 0.3, 0.1])
w_suppliers_cost = np.array([0.2, 0.5, 0.3])
w_suppliers_efficiency = np.array([0.3, 0.2, 0.5])

# 层次总排序
# 最终得分 = 质量权重 * 方案对质量权重 + 成本权重 * 方案对成本权重 + 效率权重 * 方案对效率权重
final_scores = (w_criteria_geo[0] * w_suppliers_quality + 
                w_criteria_geo[1] * w_suppliers_cost + 
                w_criteria_geo[2] * w_suppliers_efficiency)

print("\n=== 层次总排序结果 ===")
suppliers = ['供应商A', '供应商B', '供应商C']
for name, score in zip(suppliers, final_scores):
    print(f"{name}: {score:.4f}")

best = suppliers[np.argmax(final_scores)]
print(f"🎯 最优选择: {best}")