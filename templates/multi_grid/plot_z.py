#! /usr/bin/env python

from zplot import *

# describe the drawing surface
import sys
ctype = 'eps'

## every pic is 60 * 40
## 170 = 150 + 20
c = canvas(ctype, title='multi_grid', dimensions=[150,190])

## global drawing config
## This name_list is corresponding to the log_dir
## tipically, a, b, c, d, o could be different solutions in comparison
## the dir shoudl be
## `---log_a/z.data
##  ---log_a/z.data
##  --- ...etc
name_list = ['b', 'a', 'd', 'h', 'o']

color_list = [
        'black',
        'darkgray',
        ]
color_list2= [
        #'red',
        #'blue',
        '0.15,0.15,0.15',
        'black',
        ]

fill_color_list = [
        '0.8,0.8,0.8',
        '0.5,0.5,0.5',
        ]


y_label_shift=[3,0]
x_label_shift=[0,2]
label_font_size = 5
vertical_label_font_size = 6
small_title_font_size=6 # annotate method
large_title_font_size=5.5 # annotate Throughput , Resource Utilization
method_title_shift=[77,0]
title_font ='Helvetica-Bold'
#method_title_font='Helvetica-Bold'
method_title_font='Helvetica'

#####
# this values may need to tune for specific data
title_shift=[0, -5]
axis_line_width = 0.6
tp_line_width = 0.6
line_width = 0.5
tic_major_size = 2.0
time_range = [0,120]
time_auto = [0, 120, 30]
time_format = '%ss'
util_y_range = [0,1]
util_label_list = [['0', 0], ['0.5',0.5], ['1',1],]
tp_y_range = [0, 90000]
tp_label_list = [['0',0] ,['30K', 30000],['60K', 60000],['90K', 90000],]
box_dim = [60,34]

# load data
i = 0
for name in name_list:
    name_list[i] = './log_' + name
    i += 1

tb_dict = {}
tb_dict['c1'] = table(file=(name_list[0] + '/z.data'))
tb_dict['c2'] = table(file=(name_list[1] + '/z.data'))
tb_dict['c3'] = table(file=(name_list[2] + '/z.data'))
tb_dict['c4'] = table(file=(name_list[3] + '/z.data'))
tb_dict['c5'] = table(file=(name_list[4] + '/z.data'))

## from the display view, the graph is from top to down, that is original is the first
## frm the zplot view, the top is the furthest from start point of this canvas
def get_coord(x,y):
    '''
    get the coord for each grid
    change the h_step, w_step for resize grid
    change col_sum, row_sum for more grid or less
    change base if only need more space under grids (like for text, legend)
    '''
    # x should start from 0
    # y should start from 0
    base = [14, 14]
    axis_interval = 10
    #h_step = 70
    #w_step = 70  # this could be like a squire for each grid
    #h_step = 44
    h_step = 44
    w_step = 58
    col_sum = 2
    row_sum = 4
    real_x =  row_sum - x -1
    real_y = y
    coord = [base[0] + real_y * (w_step + axis_interval), base[1] + real_x * (h_step)]
    print coord
    return coord



## control the order of ploting several case here
## also control which to show or not to show here
#method_list = [ 'c2', 'c3', 'c4', 'c1','c5']
method_list = [ 'c2', 'c3', 'c4', 'c5']
#method_list_title = ['C2-Name', 'C3-Name', 'C4-Name', 'C1-Name', 'C5-Name']
method_list_title = ['C2-Name', 'C3-Name', 'C4-Name', 'C5-Name']
# Leave it black if you do not want a title
#method_list_title = ['','','','','']


## legend objects
p = plotter()
L_c1 = legend()
L_c2 = legend()
L_avg = legend()
L_res = legend()

#### draw graph
for i in range(len(method_list)):
    cur_tb = tb_dict[method_list[i]]
    # throughput
    cur_d = drawable(canvas=c, xrange=time_range, yrange=tp_y_range, coord=get_coord(i,0), dimensions=box_dim)
    cur_title = ''
    cur_l = ''
    if i == 0:
        cur_title = 'Throughput(req/s) vs. Time(s)'
        cur_l = L_c2

    if i == 4:
        axis(drawable=cur_d, style='x', title=cur_title, titlesize=large_title_font_size, titlefont=title_font, titleshift=title_shift, xauto=time_auto, linewidth=axis_line_width, ticmajorsize=tic_major_size, xlabelshift=x_label_shift, xlabelfontsize=label_font_size, xlabelformat=time_format)
    else:
        axis(drawable=cur_d, style='x', title=cur_title, titlesize=large_title_font_size, titleshift=title_shift, xauto=time_auto, dolabels=False, linewidth=axis_line_width, ticmajorsize=tic_major_size)
    # axis
    axis(drawable=cur_d, style='y', ymanual=tp_label_list, ylabelshift=y_label_shift, ylabelfontsize=vertical_label_font_size, linewidth=axis_line_width, ticmajorsize=tic_major_size)

    # draw line
    p.line(drawable=cur_d, table=cur_tb, xfield='t', yfield='client_2', linecolor=color_list[1], linewidth=tp_line_width, legend=cur_l, legendtext='C2')
    if i == 0:
        cur_l = L_c1
    p.line(drawable=cur_d, table=cur_tb, xfield='t', yfield='client_1', linecolor=color_list[0], linewidth=(tp_line_width*1.2), linedash=[1,0.5], legend=cur_l, legendtext='C1')
    #####
    # utilization
    cur_d = drawable(canvas=c, xrange=time_range, yrange=util_y_range, coord=get_coord(i,1), dimensions=box_dim)
    cur_title = ''
    cur_l = ''
    if i == 0:
        cur_title = 'Utilization vs. Time(s)'
        cur_l = L_res

    if i == 4:
        axis(drawable=cur_d,style='x', title=cur_title, titlesize=large_title_font_size,titlefont=title_font,  titleshift=title_shift, xauto=time_auto, linewidth=axis_line_width, ticmajorsize=tic_major_size, xlabelshift=x_label_shift, xlabelfontsize=label_font_size, xlabelformat=time_format)
    else:
        axis(drawable=cur_d,style='x', title=cur_title, titlesize=large_title_font_size, titleshift=title_shift, xauto=time_auto, dolabels=False, linewidth=axis_line_width, ticmajorsize=tic_major_size)

    axis(drawable=cur_d,style='y', title='',  ymanual=util_label_list, ylabelshift=y_label_shift,
            xlabelshift=x_label_shift,xlabelfontsize=label_font_size, ylabelfontsize=vertical_label_font_size,
            linewidth=axis_line_width, ticmajorsize=tic_major_size, ytitle=method_list_title[i], ytitlesize=small_title_font_size, ytitleshift=method_title_shift, ytitlefont=method_title_font)
    p.verticalfill(drawable=cur_d, table=cur_tb, xfield='t', yfield='cpu_max', ylofield='cpu_min', fillcolor=fill_color_list[0], legend=cur_l, legendtext='CPU-Range')
    p.verticalfill(drawable=cur_d, table=cur_tb, xfield='t', yfield='io_max', ylofield='io_min', fillcolor=fill_color_list[1], legend=cur_l, legendtext='IO-Range')

    if i == 0:
        cur_l = L_avg
    #p.line(drawable=cur_d, table=cur_tb, xfield='t', yfield='cpu_avg', linecolor=color_list2[0], linewidth=line_width, legend=cur_l, legendtext='CPU-avg')
    p.line(drawable=cur_d, table=cur_tb, xfield='t', yfield='cpu_avg', linecolor=color_list2[0], linewidth=line_width)
    p.points(cur_d, cur_tb, xfield='t', yfield='cpu_avg', legend=cur_l, legendtext='CPU-avg',style='asterisk', fill=True, linewidth=0.25, linecolor=color_list2[0], size=0.9, where='t % 10 == 0 OR t % 10 == 0.0', fillcolor=color_list2[0])
    p.line(drawable=cur_d, table=cur_tb, xfield='t', yfield='io_avg', linecolor=color_list2[1], linewidth=line_width, legend=cur_l, legendtext='IO-avg')


small_title_font_size=5 # annotate method
legend_base_x = 8
legend_base_y = 3.2
L_c1.draw(canvas=c, coord=[legend_base_x, legend_base_y], width=3, height=3, fontsize=small_title_font_size, skipnext=1, skipspace=18, hspace=1)
L_c2.draw(canvas=c, coord=[legend_base_x+11, legend_base_y], width=3, height=3, fontsize=small_title_font_size, skipnext=1, skipspace=18, hspace=1)
L_avg.draw(canvas=c, coord=[legend_base_x+24, legend_base_y], width=3, height=3, fontsize=small_title_font_size, skipnext=1, skipspace=26, hspace=1)
L_res.draw(canvas=c, coord=[legend_base_x+72, legend_base_y], width=3, height=3, fontsize=small_title_font_size, skipnext=1, skipspace=34, hspace=1)

# finally, output the graph to a file
c.render()
