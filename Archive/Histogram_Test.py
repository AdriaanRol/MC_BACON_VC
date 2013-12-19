
hist_data=np.zeros((np.shape(B_Fields)[0],8))
for idb, B_Field in enumerate(B_Fields):
    hist, bin_edges=  np.histogram(x[:,idb],bins = 8, range = (-.5,7.5),density = True)
    hist_data[idb] = hist
data =np.transpose(hist_data)#np.array([
column_names = B_Fields
row_names =np.arange(0,8,1)
fig = plt.figure()
ax = Axes3D(fig)
lx= len(data[0])            # Work out matrix dimensions
ly= len(data[:,0])
xpos = np.arange(0,lx,1)    # Set up a mesh of positions
ypos = np.arange(0,ly,1)
xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
xpos = xpos.flatten()   # Convert positions to 1D array
ypos = ypos.flatten()
zpos = np.zeros(lx*ly)
dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = data.flatten()

ax.bar3d(xpos,ypos,zpos, dx, dy, dz, color='b',alpha =0.5)
ticksx = np.arange(0.5, np.size(B_Fields), 1)
plt.xticks(ticksx, column_names)
ticksy = np.arange(0.6, 10, 1)
plt.yticks(ticksy, row_names)
ax.set_xlabel('B-Fields')
ax.set_ylabel('Number of Gates')
ax.set_zlabel('Probabilty')

plt.show()
