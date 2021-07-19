import torch

def inference_final_set(P, F, n, out=[]):
    '''
    Input:
        P: Positions of initial node  n*3
        F: Features of initial node  n*d
        n: Max level of generated tree
    Output:
        out: Position List of generated children nodes
    ''' 
    if(n == 0):
        return out
    P_list = []
    P_list_re = []
    I_list = []
    leaf_node_list = []
    
    tmp_P = P
    tmp_F = F
    father_I = torch.zeros((1,1))
    P_list.append(P[0])

    for i in range(n):
        left_featrue, left_P, left_isleaf, right_featrue, right_P, right_isleaf = model.decoder(tmp_F, tmp_P)
        
        left_xy_new = left_P[:,:2] * tmp_P[:,2:4] + tmp_P[:,:2]
        left_P[:,:2] = left_xy_new
        left_wh_new = left_P[:,2:4] * tmp_P[:,2:4]
        left_P[:,2:4] = left_wh_new
        left_a_new = left_P[:,4] + tmp_P[:,4]
        left_P[:,4] = left_a_new
        
        right_xy_new = right_P[:,:2] * tmp_P[:,2:4] + tmp_P[:,:2]
        right_P[:,:2] = right_xy_new
        right_wh_new = right_P[:,2:4] * tmp_P[:,2:4]
        right_P[:,2:4] = right_wh_new
        right_a_new = right_P[:,4] + tmp_P[:,4]
        right_P[:,4] = right_a_new
        
        I = np.zeros(len(left_P)*2, dtype='int32')
        
        temp_I_list = []
        left_node_index = torch.zeros((len(left_P),1))
        right_node_index = torch.zeros((len(right_P),1))
        
        for j in range(len(left_P)):
            
            P_list.append(left_P[j])
            left_index =len(P_list) -1
            P_list.append(right_P[j])
            right_index =len(P_list) -1
            
            father_index = father_I[j].detach().numpy()
            father_index = int(father_index)
            temp_I = [left_index, right_index, father_index]
            
            I[2*j] = left_index
            I[2*j+1] = right_index
            left_node_index[j] = left_index
            right_node_index[j] = right_index

            temp_I_list.append(temp_I)
            
        if(temp_I_list):     
            I_list.append(temp_I_list) 
    
        tmp_F = []
        tmp_P = []
        father_I = []
        
        left_isleaf = torch.round(left_isleaf)[:,0]
        right_isleaf = torch.round(right_isleaf)[:,0]
        
        tmp_F.append(left_featrue[left_isleaf==0,:])
        tmp_P.append(left_P[left_isleaf==0,:])
        father_I.append(left_node_index[left_isleaf==0,:])
        
        tmp_F.append(right_featrue[right_isleaf==0,:])
        tmp_P.append(right_P[right_isleaf==0,:])
        father_I.append(right_node_index[right_isleaf==0,:])
        
        if(len(left_P[left_isleaf==1,:])>0):
            leaf_node_list.append(left_P[left_isleaf==1,:])
        if(len(right_P[right_isleaf==1,:])>0):
            leaf_node_list.append(right_P[right_isleaf==1,:])
        
        tmp_F = torch.cat(tmp_F, 0)
        tmp_P = torch.cat(tmp_P, 0)
        father_I = torch.cat(father_I, 0)

    P_list = torch.stack(P_list)
    leaf_node_list = torch.cat(leaf_node_list)
    return P_list, I_list, leaf_node_list

def rotate_xy_2(p, sin, cos, center):
    x_ = (p[:,0:1]-center[:,0:1])*cos-(p[:,1:2]-center[:,1:2])*sin+center[:,0:1]
    y_ = (p[:,0:1]-center[:,0:1])*sin+(p[:,1:2]-center[:,1:2])*cos+center[:,1:2]
    return np.hstack((x_, y_))

def get_box_2(P, F):
    ld = np.hstack((P[:,0:1]-F[:,0:1]/2, P[:,1:2]-F[:,1:2]/2))
    rd = np.hstack((P[:,0:1]+F[:,0:1]/2, P[:,1:2]-F[:,1:2]/2))
    ru = np.hstack((P[:,0:1]+F[:,0:1]/2, P[:,1:2]+F[:,1:2]/2))
    lu = np.hstack((P[:,0:1]-F[:,0:1]/2, P[:,1:2]+F[:,1:2]/2))
    sinO = np.sin(F[:,2:3])
    cosO = np.cos(F[:,2:3])

    ld_r = rotate_xy_2(ld, sinO, cosO, P)
    rd_r = rotate_xy_2(rd, sinO, cosO, P)
    ru_r = rotate_xy_2(ru, sinO, cosO, P)
    lu_r = rotate_xy_2(lu, sinO, cosO, P)
    if(len(P)>0):
        box_r = np.hstack((ld_r, rd_r, ru_r, lu_r)).reshape(len(P), -1, 2)
    else:
        box_r = []
    return box_r

def plot_boxes2(samples, n, m, save=False, savename='pclouds'):
    fig = plt.figure(figsize=(5*m,5*n))
    fig.set_tight_layout(True)
    for i in range(n):
        for j in range(m):
            idx = i * m + j
            ax = fig.add_subplot(n, m, idx+1)
            draw_box2(samples[idx])  
    if save:
        plt.savefig(savename)

    plt.show()

def draw_polygon_c(pc, txt, center, color):
    X, Y= pc[:, 0], pc[:,1]
    plt.plot(X, Y, c=color)
    plt.plot([X[-1],X[0]], [Y[-1],Y[0]], c=color)
    plt.axis('off')

def draw_box(box, txt, center, color):
    for i, p in enumerate(box):
        c = 'r' if color[i] else 'b'
        draw_polygon_c(p, txt[i], center[i], c)

def draw_box2(box):
    for i, p in enumerate(box):
        draw_polygon_c2(p)

def plot_boxes(samples, label, center, color, n, m, save=False, savename='pclouds'):
    fig = plt.figure(figsize=(5*m,5*n))
    fig.set_tight_layout(True)
    for i in range(n):
        for j in range(m):
            idx = i * m + j
            ax = fig.add_subplot(n, m, idx+1)
            draw_box(samples[idx], label[idx], center[idx], color[idx])  
    if save:
        plt.savefig(savename)

    plt.show()

def draw_polygon_c2(pc, color='b'):
    X, Y= pc[:, 0], pc[:,1]
    plt.plot(X, Y, c=color)
    plt.plot([X[-1],X[0]], [Y[-1],Y[0]], c=color)
    plt.axis('equal')

def draw_polygon_s(pc, w, c):
    
    X, Y= pc[:, 0], pc[:,1]
    plt.plot(X, Y, linewidth=w, color=c)
    plt.plot([X[-1],X[0]], [Y[-1],Y[0]], linewidth =w, color=c)
    plt.axis('equal')
    plt.axis('off')

def draw_box_save(box, linewidth='3', color='mediumslateblue', name='gt'): 
    fig = plt.figure(figsize=(6,6))
    for i, p in enumerate(box):
        draw_polygon_s(p, linewidth, color)
    plt.savefig(name,bbox_inches='tight',dpi=300,pad_inches=0.0)
