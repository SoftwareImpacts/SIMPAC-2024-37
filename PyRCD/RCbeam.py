# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:31:20 2022

@author: Tabish Izhar
"""
import numpy as np
import pandas as pd
import math
import plotly.graph_objects as go 
import itertools as itr 
import random
import time

class rcb():
    """
    This is a class to represent a reinforced concrete beam. It creates an object for the reinforced concrete beam on which design is to be performed as per the guidelines stated by user. 

    :param width: A handle to the :class:`PyRCD.RCbeam.rcb` that detects the width of the reinforced concrete beam in millimeters (mm). 
    :type width: int/float
    
    :param depth: A handle to the :class:`PyRCD.RCbeam.rcb` that detects the effective depth of the reinforced concrete beam in millimeters (mm). 
    :type depth: int/float

    :param length: A handle to the :class:`PyRCD.RCbeam.rcb` that detects the clear length of the reinforced concrete beam in meters (m). 
    :type length: int/float 

    :param bending_moment: A handle to the :class:`PyRCD.RCbeam.rcb` that detects the bending moment on the reinforced concrete beam in kilo-newton-meters (kNm). If the instance is int or float, it is considered as bending moment is only acting at center of the beam and zero moment at the beam's end. If the instance is list, list must represents bending moment at left end, center and right end of the beam with three elements repectively.  
    :type bending_moment: int/float/list
 
    :param shear_force: A handle to the :class:`PyRCD.RCbeam.rcb` that detects the shear forces on the reinforced concrete beam in kilo-newton (kN). If the instance is int or float, the shear force value is considered as same on either end of the beam. If the instance is list, list must represents shear force at left end, center and right end of the beam with three elements repectively.   
    :type shear_force: int/float/list

    :param torsion:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects the torsion on the reinforced concrete beam in kilo-newton-meter (kNm). This instance is to be used when user intend to design beam with torsion. Default is None, no torsion is considered. 
    :type torsion: int/float, optional

    :param defl:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects the maximum deflection of the reinforced concrete beam in millimeters (mm). This instance is to be used when user intend to check the deflection limit of the beam. By Default beam is considered safe in deflection. 
    :type defl: int/float, optional

    :param cover:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects the effective cover that is to be provided in beam in millimeter  (mm), default is 25mm. This instance is to be used when user intend to change the effective cover of the beam. Check :ref:`InputExample:Nodes Details` for more details.
    :type cover: int/float, optional    

    :param ast_provided:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects the reinforcement area provided by user in the reinforced concrete beam in square-millimeter (mm2). If the instance is int or float, it is considered as reinforcement has only been provided in the bottom of the beam. If the instance is list, list must represents rebar areas provided at left end, center and right end of the beam repectively.  Check :ref:`InputExample:Nodes Details` for more details.
    :type ast_provided: int/float/list

    :param left_support_size:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects width of support size on left end of the beam in mllimeter (mm), default is 400 mm. This instance is used to perform detailing of the beam. Check :ref:`InputExample:Nodes Details` for more details.
    :type left_support_size: int/float, optional

    :param right_support_size:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects width of support size on right end of the beam in mllimeter (mm), default is 400 mm. This instance is used to perform detailing of the beam. Check :ref:`InputExample:Nodes Details` for more details.
    :type right_support_size: int/float, optional

    :param left_end_continous:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects wheather the beam is continous on the left end or not. Default is False (i.e. Beam is not continous). This instance is used to perform practical detailing of the beam. Check :ref:`InputExample:Nodes Details` for more details.
    :type left_end_continous: boolean, optional

    :param right_end_continous:  A handle to the :class:`PyRCD.RCbeam.rcb` that detects wheather the beam is continous on the right end or not. Default is False (i.e. Beam is not continous). This instance is used to perform practical detailing of the beam. Check :ref:`InputExample:Nodes Details` for more details.
    :type right_end_continous: boolean, optionall

    """

    def __init__(self, width, depth, length,  bending_moment, shear_force, torsion= None,  defl= None, cover= 25, ast_provided= None, left_support_size= 400, right_support_size= 400, left_end_continous= False, right_end_continous= False):

        if not isinstance(width, (int, float)):
            raise TypeError ("Type of 'width' must be int or float in millimiter (mm)") 
        self.b= width
        

        if not isinstance(depth, (int, float)):
            raise TypeError ("Type of 'depth' must be int or float in millimiter (mm)")
        self.d= depth
        

        if not isinstance(length, (int, float)):
            raise TypeError ("Type of 'length' must be int or float in meters (m)")
        self.l= length     

        if not isinstance(bending_moment, (int, float,list)):
            raise TypeError ("Type of 'bending moment' must be int or float or list with three values representing bending moment at left end, bending moment at center and bending moment at right end respectively. Values must be in kilo-Newtom-meter (kN-m).  ")
        
        if isinstance(bending_moment, (int, float)): 
            self.BM_center= bending_moment
            self.BM_left= 0
            self.BM_right= 0

        if isinstance(bending_moment, (list)): 
            if len(bending_moment) !=3:
                raise Exception ("Length of the list must be 3 representing bending moment at left end, center and right end of the beam repectively. Values must be in kilo-Newtom-meter (kN-m). ")
            
            for i in bending_moment:
                if not isinstance(i, (int, float)):
                    raise TypeError ("Type of 'bending moment' in list must be int or float. Values must be in kilo-Newtom-meter (kN-m). ")
                
            self.BM_center= bending_moment[1]
            self.BM_left= bending_moment[0]
            self.BM_right= bending_moment[2]


        if not isinstance(shear_force, (int, float,list)):
            raise TypeError ("Type of 'shear force' must be int or float or list with three values representing shear force at left end, shear force at center and shear force at right end respectively. Values must be in kilo-Newton (kN). ")
        
        if isinstance(shear_force, (int, float)): 
            self.Vu= shear_force *1000
            self.Vu_left= 0
            self.Vu_right= 0
            self.shear_type= 0

        if isinstance(shear_force, (list)): 
            if len(shear_force) !=3:
                raise Exception ("Length of the list must be 3 representing shear force at left end, center and right end of the beam repectively. Values must be in kilo-Newton (kN). ")
            
            for i in shear_force:
                if not isinstance(i, (int, float)):
                    raise TypeError ("Type of 'shear force' in list must be int or float. Values must be in kilo-Newton (kN).")
                
            self.Vu= shear_force[1] *1000
            self.Vu_left= shear_force[0] *1000
            self.Vu_right= shear_force[2] *1000
            self.shear_type= 1      


        if defl is not None:
            if not isinstance(defl , (int, float)):
                raise TypeError ("'deflection' of the member must be of int or float type in millimiter (mm).")
            self.defl= defl
        else:
            self.defl= 2


        self.ast_provided= False
        if ast_provided is not None:
            self.ast_provided= True
            if not isinstance(ast_provided, (int, float,list)):
                raise TypeError ("Type of 'ast_provided' must be int or float or list with three values representing rebar areas provided at left end, at center and at right end of the beam respectively. Values must be in square-millimeter (mm2).  ")
            
            if isinstance(ast_provided, (int, float)): 
                self.Ast_center= ast_provided
                self.Ast_left= 0
                self.Ast_right= 0
                self.ast_provided_type= 0

            if isinstance(ast_provided, (list)): 
                if len(ast_provided) !=3:
                    raise Exception ("Length of the list must be 3 representing rebar areas provided at left end, center and right end of the beam repectively. Values must be in square-millimeter (mm2). ")
                
                for i in ast_provided:
                    if not isinstance(i, (int, float)):
                        raise TypeError ("Type of 'rebar area' in list must be int or float. Values must be in square-millimeter (mm2). ")
                    
                self.Ast_center= ast_provided[1]
                self.Ast_left= ast_provided[0]
                self.Ast_right= ast_provided[2]
                self.ast_provided_type= 1
                  
        self.cover= cover
  
        self.total_depth= self.d + self.cover

        self.torsion= torsion

        
        self.side_bar= False

        self.left_support_size= left_support_size
        self.right_support_size = right_support_size 
        self.left_end_continous= left_end_continous 
        self.right_end_continous= right_end_continous


        self.beam_status_frame= pd.DataFrame()    # Creating Dataframe

        self.rebar_config()

        self.top_bars_frame= pd.DataFrame()
        # self.bottom_bars_frame= pd.DataFrame()
        # self.beam_shear_detail_frame= pd.DataFrame()
        self.plotting_status= False
        self.optimization_status= False

    def check_beam(self):
        """This function of :class:`PyRCD.RCbeam` objects performs design check for reinforced concrete beam for the given crosssection, rebars and foces provided by user. It also suggest improvement if beam fails in some checks. 

        :param: None
        """

        self.__check_cross_section() 

        if self.ast_provided== False:
            raise Exception("Please provide the reinforcement areas of the beam in order to check the design.")

        if self.ast_provided_type== 0:
            if self.Ast_center < self.Ast[0]:
                self.beam_status[["Rebar_Check"]] = "Fail"
            else: 
                self.beam_status[["Rebar_Check"]]= "Pass"

        if self.ast_provided_type== 1:
            if self.Ast_center < self.Ast[0]:
                self.beam_status[["Rebar_Check"]] = "Fail"
            else: 
                self.beam_status[["Rebar_Check"]]= "Pass"

            if self.Ast_left < self.Ast[1]:
                self.beam_status[["Rebar_Check"]] = "Fail"
            else: 
                self.beam_status[["Rebar_Check"]]= "Pass"

            if self.Ast_right < self.Ast[2]:
                self.beam_status[["Rebar_Check"]] = "Fail"           
            else: 
                self.beam_status[["Rebar_Check"]]= "Pass"
        
        self.__shear_check()
        self.rebar_detail= "Designing Not done. Please perform Design first."
        self.shear_detail= "Designing Not done. Please perform Design first."

        # return (self.beam_status)

    def dsgbeam(self):
        """This function of :class:`PyRCD.RCbeam` objects performs design for reinforced concrete beam for the given cross-section and foces. It check the provided depth and evaluates the reinforcement bars and combination along with shear bars. 

        :param: None
        """
        self.__check_cross_section()

        if self.status == 0:
            if self.beam_status.iloc[0,0] == "Fail":
                print ("Beam failed in deflection. Increase the depth of the beam")

            if self.beam_status.iloc[0,1] == "Fail":
                print ("Beam failed in lateral statbility. Increase the width of the beam.")

            if self.beam_status.iloc[0,2] == "Fail":
                print ("Beam failed in moment check. More depth and width is required, increase the depth or width of the beam.")

            if self.beam_status.iloc[0,4] == "Fail":
                print ("Beam failed in reinforcement requirement as its more than the maximum limit. More depth or width is required, increase the depth or width or grade of concrete or grade of steel of the beam.")

            raise Exception(" Beam design has failed in the safety checks. Increase the dimension of the RC beam.")

        self.__rebars_design()
        self.beam_status[["Rebar_Check"]]= "Pass"

        self.__shear_check()

        if self.beam_status.iloc[0,5] == "Fail":
            raise Exception("Beam has failed in shear. Required shear stress is more than maximum allowed. Increase the width or depth of the beam")

        self.plotting_status= True
        self.__objCalculation()

    def __check_cross_section (self, bb=None, dd=None):
        
        if bb==None and dd== None:
            b= self.b
            d= self.d

        if bb!=None and dd== None:
            self.b= bb
            b= self.b
            d= self.d

        if bb==None and dd!= None:
            self.d= dd
            b= self.b
            d= self.d

        if bb!=None and dd!= None:
            self.b= bb
            self.d= dd
            b= bb
            d= dd

        self.constraint() 

        l= self.l

        status= 1
        BMC = self.BM_center
        BML= self.BM_left
        BMR= self.BM_right

        max_bm= max(abs(BMC), abs(BML), abs(BMR))
        min_bm= min(abs(BMC), abs(BML), abs(BMR))

        D= d+ self.cover
        T= self.torsion

        self.Vt= 0

        if T != None:
            self.Mt= T* (1 + (D/b))/1.7
            self.Vt= T*1.6/ b

            if max_bm > self.Mt:

                if BMC < 0:
                    BMC = BMC - self.Mt
                else:
                    BMC = BMC + self.Mt 

                if BML < 0:
                    BML = BML - self.Mt
                else:
                    BML = BML + self.Mt 

                if BMR < 0:
                    BMR = BMR - self.Mt
                else:
                    BMR = BMR + self.Mt    


            if D >= 450:
                self.side_bar= True

        if D >= self.side_rebar_depth:
            self.side_bar= True


        beam_status_cols= ["Deflection_Check", "Lateral_Stability_Check", "Moment_Check", "Rebar_Check", "Rebar_Max_Check", "Shear_Check"]

        beam_status= pd.DataFrame(columns= beam_status_cols, index=[1])

        beam_status.iloc[:,:]= "Not Checked"


        defl = self.defl          
        fc= self.fck
        fy= self.fy  
        ast_max= self.ast_max
        defl_lim= self.defl_lim
        
        if defl> defl_lim or defl> 20:    # deflection checking
            beam_status.Deflection_Check= "Fail" 
            status= 0
        else: 
            beam_status.Deflection_Check= "Pass"

        if (l*1000)> self.lateral_stability:    # lateral stability checking
            beam_status.Lateral_Stability_Check= "Fail"
            status= 0
        else: 
            beam_status.Lateral_Stability_Check= "Pass"

        Mu= max_bm*pow(10,6)

        self.mulim_ast_calculation(Mu,BMC,BML,BMR)

        if abs(Mu) > self.Mu_lim:
            beam_status.Moment_Check= "Fail"
            status= 0
        else: 
            beam_status.Moment_Check= "Pass"

        if max(abs(self.Ast)) > ast_max:
            beam_status.Rebar_Max_Check= "Fail"
            status= 0
        else: 
            beam_status.Rebar_Max_Check= "Pass"  

        self.status= status 
        self.beam_status= beam_status  
        self.pt= abs((100*self.Ast/(b*d)))
        self.constructability()


# Shear Reinforcement Calculation   
    def __shear_check(self):

        Vu= self.Vu
        Vu_left= self.Vu_left
        Vu_right= self.Vu_right

        b= self.b
        d= self.d

        ptt= self.pt
        fc= self.fck

        if fc > 40:
            fc= 40

        self.beam_shear_detail= pd.DataFrame()

        tc_max= self.tc_max
         
        tc_pd= self.tc_pd
        

        s_fc=str(fc)
        index_no = tc_pd.columns.get_loc(s_fc)
        
        xxx=[]
        for pt in ptt:
            exactmatch = tc_pd[tc_pd['pt'] == pt]
            if not exactmatch.empty:
                exact_ind= exactmatch.index
                xx= tc_pd.iloc[exact_ind,index_no]                                                  # Final tc value after interpolation
            
            if pt >3:
                xx= 3

            if pt < 0.15:
                xx = tc_pd.at[0,s_fc]

            if (pt > 0.15) and (pt < 3):                
                lowerneighbour_ind = tc_pd[tc_pd['pt'] < pt]['pt'].idxmax()
                upperneighbour_ind = tc_pd[tc_pd['pt'] > pt]['pt'].idxmin()
                yy= tc_pd.iloc[lowerneighbour_ind,index_no]
                zz= tc_pd.iloc[upperneighbour_ind,index_no]

                m = (zz - yy) / (tc_pd.iloc[upperneighbour_ind,0] - tc_pd.iloc[lowerneighbour_ind,0])
                xx = (pt - tc_pd.iloc[lowerneighbour_ind,0]) * m + yy                           # Final tc value after interpolation
            
            xxx.append(xx)


        new_val= xxx[0]
        xxx[0]= xxx[1]
        xxx[1]= xxx[2]
        xxx[2]= new_val
        self.tc=xxx
                   
        if self.shear_type== 0:

            Vu= abs(Vu) + self.Vt
            
            self.tv = Vu/(b*d)
        
            if (self.tv > tc_max):
                self.beam_status.Shear_Check= "Fail"
            else: 
                self.beam_status.Shear_Check= "Pass"

            self.tv_left = self.tv
            self.tv_right = self.tv
            self.tv= 0
        
        if self.shear_type== 1:

            Vu= abs(Vu) + self.Vt
            Vu_left= abs(Vu_left) + self.Vt
            Vu_right= abs(Vu_right) + self.Vt

            self.tv= Vu/(b*d)
            self.tv_left = Vu_left/(b*d)
            self.tv_right = Vu_right/(b*d)
        
            if (self.tv_left > tc_max):
                self.beam_status.Shear_Check= "Fail"
            else: 
                self.beam_status.Shear_Check= "Pass"

            if (self.tv > tc_max):
                self.beam_status.Shear_Check= "Fail"
            else: 
                self.beam_status.Shear_Check= "Pass"

            if (self.tv_right > tc_max):
                self.beam_status.Shear_Check= "Fail"
            else: 
                self.beam_status.Shear_Check= "Pass"


        self.actual_shear_stress= [self.tv_left, self.tv_right, self.tv]

        
        beam_shear_detail = self.__shear_bars_design()

        self.beam_shear_detail= pd.concat([self.beam_shear_detail, beam_shear_detail ])

        self.shear_detail= self.beam_shear_detail.copy()


    def __rebars_design(self):

        Design_Cost_rebar_pd = pd.DataFrame()
        self.top_bars= pd.DataFrame()
        self.bottom_bars= pd.DataFrame()

        for ii,i in enumerate (self.Ast):
            
            Design_Cost_rebar= self.__tension_rebar_design(i,self.max_bars[ii])           #, Design_Build_rebar

            #Design_Build_rebar_pd= pd.concat([Design_Build_rebar_pd, Design_Build_rebar])

            Design_Cost_rebar_pd= pd.concat([Design_Cost_rebar_pd, Design_Cost_rebar])

        self.REBAR_CHECK= Design_Cost_rebar_pd

        self.DCRpd= Design_Cost_rebar_pd
        top_bars_pd = Design_Cost_rebar_pd.iloc[1:,:]
        bottom_bars_pd = Design_Cost_rebar_pd.iloc[0,:].to_frame().T
        
        top_bars= Design_Cost_rebar_pd.iloc[1:,5:]
        top_bars_np= top_bars.iloc[:,0:6].to_numpy()

        x_len,y_len= np.shape(top_bars_np)
        success= False

        for ii in range (0,y_len,2):
            for jj in range (0,y_len,2):
                if top_bars_np[0,ii+1]>=2:
                    if top_bars_np[0,ii]== top_bars_np[1,jj]:
                        if top_bars_np[1,jj+1]>=2:
                            success= True
                            common_bar= top_bars_np[0,ii]
                            continous_bar = top_bars_np[0,ii]

        if success==False:
            if top_bars.iat[0,1] >=2:
                top_left = top_bars.iat[0,0] 

            if top_bars.iat[0,1] <2 and top_bars.iat[0,3] >=2:
                top_left = top_bars.iat[0,2]

            if top_bars.iat[0,1] <2 and top_bars.iat[0,3] <2 and top_bars.iat[0,5] >=2:
                top_left = top_bars.iat[0,4]


            if top_bars.iat[1,1] >=2:
                top_right = top_bars.iat[1,0] 

            if top_bars.iat[1,1] <2 and top_bars.iat[1,3] >=2:
                top_right = top_bars.iat[1,2]

            if top_bars.iat[1,1] <2 and top_bars.iat[1,3] <2 and top_bars.iat[1,5] >=2:
                top_right = top_bars.iat[1,4]
        

            if top_left < top_right: 
                common_bar= top_left
                continous_bar = top_left
                to_be_fixed= 2
            
            if top_left > top_right: 
                common_bar= top_right
                continous_bar = top_right
                to_be_fixed= 1
        

        if success== True:
            top_bars_pd.loc[:, ["Continous Bar","Number of Bars"]]= " "
            bottom_bars_pd.loc[:, ["Continous Bar","Number of Bars"]]= " "            
            top_bars_pd.loc[:,["Continous Bar"]]= continous_bar
            top_bars_pd.loc[:,["Number of Bars"]]= 2
            

            for i in range (5,11,2):
                if bottom_bars_pd.iat[0, i+1] >=2:
                    min_size_bottom= bottom_bars_pd.iat[0,i]
                    break

            bottom_bars_pd.loc[:,["Continous Bar"]]= min_size_bottom
            bottom_bars_pd.loc[:,["Number of Bars"]]= 2

        if success == False:
            # print ("Check Line 699 as its not getting optmized if its reaching here")
            DCR= self.__tension_rebar_design(self.Ast[to_be_fixed],self.max_bars[to_be_fixed],common_bar )

            # self.DCR= DCR
            # self.TBP= top_bars_pd

            top_bars_pd.iloc[to_be_fixed-1,:]= DCR.iloc[0,:]
            # top_left = top_bars_pd.iat[0,5]

            top_bars_pd.loc[:, ["Continous Bar","Number of Bars"]]= " "
            bottom_bars_pd.loc[:, ["Continous Bar","Number of Bars"]]= " "            
            top_bars_pd.loc[:,["Continous Bar"]]= continous_bar
            top_bars_pd.loc[:,["Number of Bars"]]= 2

            for i in range (5,11,2):
                if bottom_bars_pd.iat[0, i+1] >=2:
                    min_size_bottom= bottom_bars_pd.iat[0,i]
                    break

            bottom_bars_pd.loc[:,["Continous Bar"]]= min_size_bottom
            bottom_bars_pd.loc[:,["Number of Bars"]]= 2


        self.top_bars= pd.concat([self.top_bars, top_bars_pd ])
        
        self.bottom_bars= pd.concat([self.bottom_bars, bottom_bars_pd ])
        
        self.rebar_detail=  pd.concat([self.bottom_bars, self.top_bars])

        self.pt= ((100*self.rebar_detail['Total_Area (mm2)']/(self.b*self.d))).to_list()

        self.side_bar_detail= 0

        if self.side_bar== True:          
            
            area_required= 0.05*self.b*(self.total_depth)/1000

            if area_required < 113.04:
                bar = 12
                area_p= 113.04

            if (area_required > 113.04) and (area_required < 201):
                bar = 16
                area_p= 201

            if (area_required > 201) and (area_required < 314):
                bar = 20
                area_p= 314
            
            bar_list= [bar, bar]
            face= ["Left Face", "Right Face"]

            self.side_bar_detail= pd.DataFrame({'Face': face, 'Area Required (mm2)': area_required, 'Area Provided (mm2)': [area_p,area_p],'Total_Bars': [1,1], 'Bar (mm)': bar_list} )
            
            
        # Development Length
        self.rebar_detail[["Development Length (mm)"]]= " "

        self.ld_calculation()

        self.rebar_detail.iloc[1, 13] = self.Ldlc
        
        self.rebar_detail.iloc[2, 13] = self.Ldrc

        self.rebar_detail.iloc[0, 13] = self.Ldb

        self.rebar_detail.index= [ "Bottom Rebar", "Top Left Support", "Top Right Support"]

#------------------------------------------------------------------------------

    def __tension_rebar_design(self, Ast, max_bars, common= None):

        b= self.b
        ast= abs(Ast)
        
        rebar_pd= self.rebar_pd.copy()

        rebars_list= self.rebars_list.copy()

        List_of_N_1 = list(itr.combinations(rebars_list, 1))
        
        List_of_N_2 = list(itr.combinations(rebars_list, 2))
        List_of_N_3 = list(itr.combinations(rebars_list, 3))    
        List_of_N= List_of_N_1 + List_of_N_2 + List_of_N_3
        
        T0 = 2500
    
        major = 75
        minor = 100
        alpha = 0.9988
        n = 1           # no of solutions accepted
        Temp = []
        Min_Cost = []
        optimized_area= []
        list_bars= []
        solutions= []
        record_best_fitness =[]
        index_list=[]


        for i in range (5000):
            ran_initial = np.random.randint(0,len(List_of_N))
            aa1= List_of_N[ran_initial][0]

            if len(List_of_N[ran_initial]) ==1:
                sum_init = rebar_pd[aa1].values[0]

            if len(List_of_N[ran_initial]) ==2:
                aa2= List_of_N[ran_initial][1]
                sum_init = rebar_pd[aa1].values[0]+ rebar_pd[aa2].values[0]

            if len(List_of_N[ran_initial]) >2:
                aa2= List_of_N[ran_initial][1]
                aa3= List_of_N[ran_initial][2]
                sum_init = rebar_pd[aa1].values[0] + rebar_pd[aa2].values[0] + rebar_pd[aa3].values[0]

            init_diff= sum_init-ast
                
            if  sum_init > ast:
                break
        ran= 1            
        best_fitness= init_diff
        best_bars= 12
        
        rand1= [1,2,3,4,5,6]
        for i in range (major):
            if len(List_of_N) < 2:
                break

            for j in range (minor):

                if len(List_of_N) < 2:
                    break

                # ran0 =  random.choice(rand1)

                if i==0 and j< len(List_of_N_1):
                    ran_1=0
                else:
                    ran_1= random.randint(0,len(List_of_N)-1)  

                if ran_1 > (len(List_of_N)-1) or ran_1<0:
                    print ("Here")
                    continue
                

                A1 = List_of_N[ran_1][0]
                
                bar1 = rebars_list.index(A1)        # rebar_pd.columns.get_loc(A1)
                

                op11= int(bar1/4) 
                op12= 1+bar1-(int(bar1/4)*4) 
                sum_new = rebar_pd[A1].values[0]
                tt_bars= op12
            
                if len(List_of_N[ran_1]) ==2:
                    A2 = List_of_N[ran_1][1]
                    bar2 = rebars_list.index(A2)
                    op22= 1+bar2-(int(bar2/4)*4) 

                    sum_new = rebar_pd[A1].values[0]+ rebar_pd[A2].values[0]
                    tt_bars= op12 + op22
            
                if len(List_of_N[ran_1]) ==3:

                    A2 = List_of_N[ran_1][1]
                    bar2 = rebars_list.index(A2)
                    op22= 1+bar2-(int(bar2/4)*4) 

                    A3= List_of_N[ran_1][2]
                
                    bar3 = rebars_list.index(A3) 
                    op32= 1+bar3-(int(bar3/4)*4) 

                    sum_new = rebar_pd[A1].values[0] + rebar_pd[A2].values[0] + rebar_pd[A3].values[0]
                    tt_bars= op12+ op22+ op32
             
      
                current_solution= List_of_N[ran_1]
                current_fitness= sum_new-ast
                current_bars = tt_bars

                E = (current_fitness - best_fitness)
                

                if sum_new <ast:
                    List_of_N.pop(ran_1)
                    continue


                if (current_fitness > best_fitness) :  
                    p = math.exp(-E/ (T0))	
                # make a decision to accept the worse solution or not
                    if random.random()<p:
                        accept = True 		# this worse solution is accepted
                    else:
                        accept = False 		# this worse solution is not accepted
                    
                else: 
                    accept =True     # this accepts better solution 

                if accept ==True:
                    
                    best_solution = current_solution   # update the best solution
                    
                    best_fitness = current_fitness
                    best_bars = current_bars

                    n=n+1				# count solutions accepted

                    solutions.append(best_solution)
                    optimized_area.append(sum_new)
                    record_best_fitness.append(best_fitness)
                    Temp.append(T0)
                    list_bars.append(best_bars)
                    T0 = T0*alpha
                    ran= ran_1
                    index_list.append(ran_1)

                T0 = T0*alpha
                List_of_N.pop(ran_1)
            
            Min_Cost.append(init_diff)
        
            T0 = alpha*T0
        

        Design_Cost_rebar= self.__rebar_construct(record_best_fitness,solutions,optimized_area,list_bars, max_bars, ast,common= common)
        
        # Design_Cost_rebar= self.__rebar_without_construct_but_practical(record_best_fitness,solutions,optimized_area,list_bars, max_bars, ast,common= common)

        return Design_Cost_rebar
    


    def __shear_bars_design(self):
        
        tc= self.tc
        tv= self.actual_shear_stress                 #self.actual_shear_stress

        co= self.cover
        fy_shear = self.fy_shear
        den_steel= 76.8195          #kN/m3

        l_eff= (self.l*1000)-100             # 50 mm on each side
        b= self.b
        d= self.d

        List_of_N= self.List_of_N_str.copy()
        reb_list= self.reb_list.copy()
        rebars_dia= self.rebars_dia.copy()
        rebar_legs= self.rebar_legs.copy()

        permissible_max_spacing= self.permissible_max_spacing

        total_sum_list= []
        dia_combo= []
        leg_combo=[]
        count= 0
        for i in List_of_N:
            if len(i)==1:
                total_sum_list.append(i[0])
                Aw_index= reb_list.index(i[0])
                dia=rebars_dia[Aw_index]
                leg= rebar_legs[Aw_index]
                dia_combo.append([dia])
                leg_combo.append([leg])
                count= count +1 
            else:
                sum= i[0]+ i[1]
                total_sum_list.append(sum)
                Aw_index1= reb_list.index(i[0])
                Aw_index2= reb_list.index(i[1])
                
                leg1= rebar_legs[Aw_index1]
                leg2= rebar_legs[Aw_index2]
                legs= [leg1,leg2]
                
                dias= [rebars_dia[Aw_index1], rebars_dia[Aw_index2]]
                dia_combo.append(dias)
                leg_combo.append(legs)


        min_spacing_shear = self.min_space_between_stirrups 


        shear_detail= pd.DataFrame(columns= ["Design Shear Stress (td)", "Dia (mm)", "Leg", "Spacing (mm)", "Number of Bars", "Cutting Length (mm)", "Hook Length"], index=["Left Support",  "Right Support", "Center", ])

        S= 0.25* l_eff

        j= 0
        tc_i= 0
        for i in tv:
            
            td= i-tc[tc_i]

            if td < 0 :
                td= 0.001

            Vd= td*b*d
            spacing=[]
            Cost_min_index= []
            final_dia= []
            final_leg= []
            Awf= total_sum_list[len(total_sum_list)-1]
            pop_list= []

            for i in range (0, len(total_sum_list)-1):
                status= 1
                pop_status= 0
                Aw= total_sum_list[i]
                
                if i <=(count-1):
                    lggs= leg_combo[i][0]
                    dias= [dia_combo[i][0]]

                    leggs= [int (leg_combo[i][0])]
                    if lggs == 1:
                        pop_status= 1
                        pop_list.append(i)
                else: 

                    lggs= leg_combo[i][0] + leg_combo[i][1]
                    leggs= [int(leg_combo[i][0]) , int(leg_combo[i][1])]
                    dias= [leg_combo[i][0], leg_combo[i][1]]
                    
                    if leg_combo[i][0] ==1 and leg_combo[i][1] ==1:
                        lggs= 1
                        pop_status= 1
                        pop_list.append(i)

                    if dia_combo[i][0] ==dia_combo[i][1] :
                        lggs= 1
                        if pop_status== 0:
                            pop_status= 1
                            pop_list.append(i)


                sv_max= (Aw*0.87*fy_shear)/(0.4*b)


                if (permissible_max_spacing)> sv_max:                               # MAx SPacing of stirrups
                    max_spacing_shear= sv_max
                else:
                    max_spacing_shear= permissible_max_spacing

                # s_shear= self.shear_bar_spacing_calculation()

                s_shear= (0.87*Aw*fy_shear*d)/(Vd)

                s_shear= int(s_shear/5) *5

                if s_shear > max_spacing_shear:
                    s_shear= max_spacing_shear 
                    
                if s_shear <= min_spacing_shear:
                    status= 0
                    continue

                if (status==1) and (Aw < Awf) and (lggs !=1) and (pop_status== 0):
                    Awf= Aw
                    Cost_min_index.append(i)
                    spacing.append(s_shear)
                    final_dia.append(dias)
                    final_leg.append(leggs)
            
            bar1= (S/ spacing[0])+1
            
            if not isinstance(bar1, int):
                bar= math.ceil(bar1)
            else:
                bar=bar1

            if j ==2:

                l_remaining= l_eff- ( (shear_detail.iat[0, 3]*(shear_detail.iat[0, 4]-1)) +  (shear_detail.iat[1, 3]*(shear_detail.iat[1, 4]-1))) 
                space= math.ceil(((l_remaining/ spacing[0]))) 
                
                spacing[0]= l_remaining/space
                bar= space-1

                if spacing[0] < (max(shear_detail["Spacing (mm)"])):
                    for kkk in range (10):
                        bar= bar-1
                        
                        new_space= l_remaining/bar
                        if (new_space > (max(shear_detail["Spacing (mm)"]))):
                            if new_space <=300:
                                spacing[0]= new_space
                                break
                            if new_space >300:
                                spacing[0]= 300
                                break
                

            if td == 0.001:
                td= 0


            if final_dia[0] == 8:
                h_l= 105
            elif final_dia[0] == 10:
                h_l = 130
            elif final_dia[0] == 12:
                h_l = 155

            #cutting length calclation
            cutting_length_single= []

            for dd in final_dia:
                if len(dd)<2:
                    if dd[0] == 8:
                        h_l= 105
                    elif dd[0] == 10:
                        h_l = 130
                    elif dd[0] == 12:
                        h_l = 155
                    cutting_length= (   ((2*(b-((2*co)-dd[0])))+(2*(d-((2*co)-dd[0]))))   +  (2*h_l)    -   (6*dd[0])  )

                if len(dd)==2:
                    for ddd in dd:
                        if ddd == 8:
                            h_l= 105
                        elif ddd == 10:
                            h_l = 130
                        elif ddd == 12:
                            h_l = 155
                        cutting_length_single.append(   ((2*(b-((2*co)-ddd)))+(2*(d-((2*co)-ddd))))   +  (2*h_l)    -   (6*ddd)  )
                    cutting_length= cutting_length_single

            shear_detail.iloc[j, 0] = td
            shear_detail.iloc[j, 1] = final_dia[0][0]
            shear_detail.iloc[j, 2] = final_leg[0][0]
            shear_detail.iloc[j, 3] = spacing[0]
            shear_detail.iloc[j, 4] = bar
            shear_detail.iloc[j, 5] = cutting_length
            shear_detail.iloc[j, 6] = h_l


            j= j+1
            tc_i= tc_i + 1 
        self.sd_new= shear_detail.copy()


        actual_shear_length = (self.sd_new.iat[0,3]*(self.sd_new.iat[0,4]-1)) + (self.sd_new.iat[1,3]*(self.sd_new.iat[1,4]-1)) + (self.sd_new.iat[2,3]*(self.sd_new.iat[2,4]+1))+ 100

        if actual_shear_length > (self.l*1000):
            difference= actual_shear_length - (self.l*1000) 
            adjustment= difference / ((self.sd_new.iat[0,4]-1) + (self.sd_new.iat[1,4]-1))
            self.sd_new.iloc[0, 3]= self.sd_new.iloc[0, 3] - adjustment
            self.sd_new.iloc[1, 3]= self.sd_new.iloc[1, 3] - adjustment

        shear_detail = self.sd_new.copy()
        return shear_detail
    
    def beam_optimization(self, nearest_value= 5):
        """This function of :class:`PyRCD.RCbeam.rcb` objects performs reinforced concrete beam multi-objective design optimization. It minimizes the cross-section along with bars maintaining the safety checks. 

        :param nearest_value: It round off the cross-section dimension to `nearest_value`. It helps maintain contructability.
        :type element: int/float
        """

        b_range = np.arange(200, 501,1)
        b_range = b_range[((b_range[:]%nearest_value)==0)]   
        d_range = np.arange(250, 651,1)
        d_range = d_range[((d_range[:]%nearest_value)==0)]  
        
        combs = np.array(np.meshgrid(b_range, d_range)).T.reshape(-1,2)
        combs= combs[combs[:,0]>(combs[:,1]*0.3)]
        combs= combs[combs[:,0]<(combs[:,1])]
        
        
        co= self.cover
        l= self.l
        T0 = 2500
        minor = 500
        alpha = 0.99
        
        Temp = []

        solutions=[]
        optimized_cross_section=[]
        record_best_fitness1 = []
        record_best_fitness2 = []
        record_best_fitness3 = []


        self.vol_concrete= []
        self.vol_rebar_steel= []
        self.vol_stirrups= []        
        self.wt_rebar_steel= []
        self.wt_stirrups= []

        self.rd_list=[]
        self.sd_list=[]
        self.total_vol_list= []

        index_solution= []

        n = 1           # no of solutions accepted
        rand1= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

        len1= len(combs)/4
        len2= len(combs)/2
        len3= 3*len(combs)/4

        for ini in range (10):
            ran11 =  np.random.randint(0,len1)
            ran22 =  np.random.randint(len1,len2)
            ran33 =  np.random.randint(len2,len3)
            ran44 =  np.random.randint(len3,len(combs)-1)
            init_fail= False
            ran_final= [ran11, ran22, ran33, ran44]
            wt_f= []
            best_fitness= 0
            total_cost_list= []
            total_co2_list= []
            
            for ran in ran_final:
                b= combs[ran,0]
                d= combs[ran,1]     

                self.__check_cross_section(b,d)

                if self.skip_status==True:
                    wt_f.append(0)
                    combs= np.delete(combs, ran, 0)
                    continue

                if self.skip_status==False:
                    if ((self.beam_status.iloc[:,:]=="Fail").any().any())== True:
                        wt_f.append(0)
                        combs= np.delete(combs, ran, 0)
                        continue
                                           
                    else:   
                        self.__rebars_design()
                        self.__shear_check()
                        self.__rebarweightcalculation()
                        rld= self.rebar_length_detail

                        shearbar_vol= 0
                        for kk in range (len(self.beam_shear_detail)):
                                dia= self.beam_shear_detail.iat[kk,1]
                                no_bar= self.beam_shear_detail.iat[kk,4]
                                cutting_len= self.beam_shear_detail.iat[kk,4]

                                shearbar_vol= shearbar_vol + ((np.round((np.pi*dia*dia/4), 4)*no_bar*cutting_len)/1000000000)            #m3

                        rebar_vol=  (sum((np.pi*rld.loc[:,"Bar"]*rld.loc[:,"Bar"]/4)*(rld.loc[:,"Length"]+rld.loc[:,"Ld"])))/ 1000000000                  #m3

                        total_conc_vol=(b*(d+co)*l/1000000)
                        conc_vol= (total_conc_vol- (rebar_vol + shearbar_vol))
                        total_weight= (self.den_s* rebar_vol*100) + (self.den_s* shearbar_vol*100) + (self.den_c*100* conc_vol)                   #in Kg
                                                              
                        wt_f.append(total_weight)


                        total_cost_steel= self.Cost_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   #INR
                        total_cost_concrete= self.Cost_concrete*conc_vol    #INR
                        total_cost_formwork= self.Cost_formwork* ( (b*l/1000) + (2*((d+co)*l/1000)))

                        total_CO2_steel= self.CO2_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   
                        total_CO2_concrete= self.CO2_concrete*(self.den_c*100* conc_vol)    
                        total_CO2_formwork= self.CO2_formwork * ( (b*l/1000) + (2*((d+co)*l/1000)))*(self.plywood_thickness/1000)*self.plywood_density



                        total_cost= total_cost_steel+ total_cost_concrete + total_cost_formwork
                        total_CO2= total_CO2_steel+ total_CO2_concrete + total_CO2_formwork

                        total_cost_list.append(total_cost)
                        total_co2_list.append(total_CO2)

                        # combs= np.delete(combs, ran, 0)


            for i in wt_f:
                if i > 0:
                    init_fail= True

 
            if init_fail== True:
                wt_f1 = [ i for i in wt_f if i >0]

                best_fitness1= min(wt_f1)
                ind= wt_f1.index(best_fitness1)
                best_solution= combs[ran_final[ind],:]

                best_fitness2= total_cost_list[ind]
                best_fitness3= total_co2_list[ind]
                
                ran= ran_final[ind]
                # combs= np.delete(combs, ran_final[ind], 0)
                break

        t1= time.time()

        set_status= 0
        Freeze= False

        while T0 > 10:

            if set_status== 1:
                count = minor
            else:
                count = 1

            if len(combs) < 2:
                break

            if Freeze==True:
                break

            for j in range(minor):
                count = count + 1 
                
                if len(combs) == 1:
                    print ("Breaking Here")
                    
                    break


                if set_status ==1:
                    ran1 =  random.choice(rand1)
                    if ran1 >10:
                        step_wise= -ran1
                    else: 
                        step_wise= ran1

                    new_ran=  ran +  step_wise 
                    ran= new_ran               
                else:
                    new_ran= np.random.randint(0,len(combs)-1)

                if new_ran > (len(combs)-1) or new_ran<0:
                    continue

                b= combs[new_ran,0]
                d= combs[new_ran,1]     

                self.__check_cross_section(b,d)

                if self.skip_status==True:
                        total_weight== 8000
                        total_cost= 35000
                        total_CO2= 3000

                if self.skip_status==False:
                        if ((self.beam_status.iloc[:,:]=="Fail").any().any())== True:
                                total_weight== 8000
                                total_cost= 35000
                                total_CO2= 3000 
                                    
                        else:    
                                self.__rebars_design()
                                self.__shear_check()
                                self.__rebarweightcalculation()
                                rld= self.rebar_length_detail

                                shearbar_vol= 0
                                for kk in range (len(self.beam_shear_detail)):
                                        dia= self.beam_shear_detail.iat[kk,1]
                                        no_bar= self.beam_shear_detail.iat[kk,4]
                                        cutting_len= self.beam_shear_detail.iat[kk,4]

                                        shearbar_vol= shearbar_vol + ((np.round((np.pi*dia*dia/4), 4)*no_bar*cutting_len)/1000000000)            #m3

                                rebar_vol=  (sum((np.pi*rld.loc[:,"Bar"]*rld.loc[:,"Bar"]/4)*(rld.loc[:,"Length"]+rld.loc[:,"Ld"])))/ 1000000000                  #m3

                                total_conc_vol=(b*(d+co)*l/1000000)
                                net_conc_vol= (total_conc_vol- ((rebar_vol + shearbar_vol)))

                                rebar_weight= (self.den_s* rebar_vol*100)
                                shearbar_weight= (self.den_s* shearbar_vol*100)

                                total_weight=  rebar_weight+ shearbar_weight + (self.den_c*100* net_conc_vol)                   #in Kg


                                total_cost_steel= self.Cost_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   #INR
                                total_cost_concrete= self.Cost_concrete*net_conc_vol    #INR
                                total_cost_formwork= self.Cost_formwork* ( (b*l/1000) + (2*((d+co)*l/1000)))

                                total_CO2_steel= self.CO2_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   
                                total_CO2_concrete= self.CO2_concrete*(self.den_c*100* net_conc_vol)    
                                total_CO2_formwork= self.CO2_formwork * ( (b*l/1000) + (2*((d+co)*l/1000)))*(self.plywood_thickness/1000)*self.plywood_density



                                total_cost= total_cost_steel+ total_cost_concrete + total_cost_formwork
                                total_CO2= total_CO2_steel+ total_CO2_concrete + total_CO2_formwork

                                total_volume= shearbar_vol + rebar_vol + net_conc_vol



                if total_weight < 0:
                    total_weight== 8000
                    total_cost= 35000
                    total_CO2= 3000 
                
                current_solution= combs[new_ran,:]
                current_fitness1= total_weight
                current_fitness2= total_cost
                current_fitness3= total_CO2

                # if T0<1000:
                #     print (total_weight)

                E1 = (current_fitness1 - best_fitness1)
                E2 = (current_fitness2 - best_fitness2)
                E3 = (current_fitness3 - best_fitness3)

                E= E1+ E2 +E3
                state=False

                if (current_fitness1 < best_fitness1) or (current_fitness2 < best_fitness2) or (current_fitness2 < best_fitness2): 
                    accept =True  
                else:
                    p = math.exp(-E/ (T0))	
                # make a decision to accept the worse solution or not
                    if random.random()<p:
                        accept = True 		# this worse solution is accepted
                        state= True
                    else:
                        accept = False 		# this worse solution is not accepted

                if accept ==True:

                    if state == False:
                        count= 0 
                        best_solution = current_solution   # update the best solution

                        best_fitness1 = current_fitness1
                        best_fitness2 = current_fitness2
                        best_fitness3 = current_fitness3

                        n=n+1				# count solutions accepted

                        solutions.append(best_solution)
                        optimized_cross_section.append(best_fitness)
                        
                        record_best_fitness1.append(best_fitness1)
                        record_best_fitness2.append(best_fitness2)
                        record_best_fitness3.append(best_fitness3)

                        self.vol_concrete.append(net_conc_vol)
                        self.vol_rebar_steel.append(rebar_vol)
                        self.vol_stirrups.append(shearbar_vol)
                        self.wt_rebar_steel.append(rebar_weight)
                        self.wt_stirrups.append(shearbar_weight)

                        self.rd_list.append(self.rebar_detail)
                        self.sd_list.append(self.beam_shear_detail)

                        self.total_vol_list.append(total_volume)
                        index_solution.append(new_ran)

                        Temp.append(T0)  

                    
                    T0 = T0*alpha
                
                combs= np.delete(combs, new_ran, 0)

            if count == minor:
                set_status= 1
                min_weight= min(record_best_fitness1)
                ind_min_weight= record_best_fitness1.index(min_weight)
                ran= index_solution[ind_min_weight]
                Freeze= True
                


            if count == (minor+minor):
                Freeze= True
                break

            T0 = T0*alpha
            


        self.optimization_result= pd.DataFrame({"Temp": Temp, "Weight (Kg)": record_best_fitness1, "Volume (m3)": self.total_vol_list, "Cost (INR)": record_best_fitness2, "CO2 (KgCO2e)": record_best_fitness3, "Solution": solutions, "Conc Vol (m3)": self.vol_concrete, "Rebar Vol (m3)": self.vol_rebar_steel, "Stirrup Vol (m3)": self.vol_stirrups, "Rebar Weight (Kg)": self.wt_rebar_steel, "Stirrup Weight (Kg)": self.wt_stirrups}  )
   
        self.plotting_status= True
        self.optimization_status= True

    def crack_width(self, distance=None, acr= None):
        """This function of :class:`PyRCD.RCbeam.rcb` objects performs crack width calculation for reinforced concrete beam. 

        :param distance: distance in millimeter fron center line of beam to a point where crack is to be calculated.
        :type element: int/float

        :param acr: distance in millimeter fron center line of beam to a point where crack is to be calculated.
        :type element: int/float        

        """
        #distance is the distance from center of beam to point where crack is to be determined
        D= self.total_depth
        Igr= self.b*D*D*D/12
        b= self.b
        bw= b                # it will be different for T beams
        yt= D/2
        ast = max(self.rebar_detail["Total_Area (mm2)"])
        co =self.cover

        if self.Ec== None:
            Ec= 5000* np.sqrt(self.fck)
        else:
            Ec= self.Ec

        Es= self.Es
        m= Es/Ec
        d= self.d

        if distance == None:
            distance= D/2

        aa= b/2
        bb= m*ast
        cc= -m*ast*d

        n_x= (np.roots([aa,bb,cc]))  # neutral axis

        if n_x > D/2:
            print ("Warning: Section is over reinforced")
            a1= distance - (n_x- (D/2))
        else:
            a1= distance + ((D/2)- n_x)


        z= d- (n_x/3)

        Ir= (b*n_x*n_x*n_x/3) + (m*ast*(d-n_x)*(d-n_x))

        Ms= max(abs(self.BM_center), abs(self.BM_left), abs(self.BM_right))

        fcs= (Ms*(d-n_x))/Ir


        Ecs = fcs/Ec            #strain in concrete at steel level

        fcr= 0.7* np.sqrt(self.fck)

        Mr= fcr*Igr/yt

        E1= (Ecs*(a1)) / (d-n_x)
        
        Em= E1-  (  (b* (D-n_x) * (a1)) / (3*Es*ast* (d-n_x))  )

        bar1= self.rebar_detail.iat[0,5]
        
        max_bar= max([self.rebar_detail.iat[0,5],self.rebar_detail.iat[0,7],self.rebar_detail.iat[0,9]])

        if acr ==None:
            acr_corner=  np.sqrt((co*co)+ (co*co)) - (bar1/2)

            space= ((b-(2*co))/ (self.rebar_detail.iat[0,4] -1))/2

            acr_edge_below_spacing= np.sqrt((space*space)+ (co*co))- (bar1/2)

            Wcr_corner= (3*acr_corner*Em) / (1+ ((2* (acr_corner- (co-(max_bar/2) )))/ (D-n_x)))

            Wcr_edege= (3*acr_edge_below_spacing*Em) / (1+ ((2* (acr_edge_below_spacing- (co-(max_bar/2) )))/ (D-n_x)))

            if Wcr_corner>= Wcr_edege:
                Wcr= Wcr_corner
            else:
                Wcr= Wcr_edege
        else:
            Wcr= (3*acr*Em) / (1+ ((2* (acr- (co-(max_bar/2) )))/ (D-n_x)))

        return Wcr


        # Ieff= Ir/ (1.2 - ( (Mr/M) * (z/d) * (1- (n_x/d)) * (bw/b) ))


        # status = 0
        # if Ieff < Igr:
        #     print ("Condition is satisfied")
        #     status = 1

    def constraint(self):
        """This function of :class:`PyRCD.RCbeam.rcb` objects initialized the **safety checks** as constraints for design and optimization of RC beam. By default, it is set as per Indian Standard IS456:2000. It can be canged as per the guideline user aim to follow. 

        :param: None
        :WARNING: Do not change the variable names
        """
        self.fck= 25                            # Grade of Concrete in N/mm2    i.e. M25
        self.fy= 500                            # Grade of Reinforcement Bar Steel in N/mm2    i.e. Fe500
        self.fy_shear= 500                      # Grade of Shear Bar Steel in N/mm2    i.e. Fe500

        self.den_c= 24                          # 24kN/m3
        self.den_s= 78.5                        # 78.5kN/m3
        self.Es= 200000                              # Modulus of Elasticity for Steel
        self.Ec= 5000* np.sqrt(self.fck)             # Modulus of Elasticity for Concrete
        self.nominal_size_aggregate= 20


        # self.Cost_steel_ref= 99.155               # Indian Rupee per kg

        self.Cost_concrete= 7783.65              # Indian Rupee per cum
        self.Cost_steel= 89.65                   # Indian Rupee per kg
        self.Cost_formwork= 608.35              # Indian Rupee per sqm Pg.135
        self.plywood_thickness= 12                         # mm 
        self.plywood_density= 650                # Kg/m3

        self.CO2_concrete= 0.129                # kgCO2e per kg
        self.CO2_steel= 1.99                    # kgCO2e per kg
        self.CO2_formwork= 0.681                # kgCO2e per kg Plywood

        self.defl_lim= min((self.l*1000/350),20)                                      #Deflection Limit
        self.ast_min = (85*self.b*self.d) / (self.fy*100)                   #Reinforcement Bar Minimum Limit
        self.ast_max = (4*self.b*self.d) / 100                                        #Reinforcement Bar Maximum Limit
        self.lateral_stability= min([(60*self.b),(250*self.b*self.b/self.d)])           #Lateral Stability Check

        self.side_rebar_depth= 750                          # Depth above which torsion rebar is required
        # Design Shear Strength Table
        tc_table = {'pt':[0.15,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3],
            '20':[0.28,0.36,0.48,0.56,0.62,0.67,0.72,0.75,0.79,0.81,0.82,0.82,0.82],
            '25':[0.29,0.36,0.49,0.57,0.64,0.70,0.74,0.78,0.82,0.85,0.88,0.90,0.92],
            '30':[0.29,0.37,0.50,0.59,0.66,0.71,0.76,0.80,0.84,0.88,0.91,0.94,0.96],
            '35':[0.29,0.37,0.50,0.59,0.67,0.73,0.78,0.82,0.86,0.90,0.93,0.96,0.99],
            '40':[0.30,0.38,0.51,0.60,0.68,0.74,0.79,0.84,0.88,0.92,0.95,0.98,1.01]}  
        self.tc_pd= pd.DataFrame(tc_table)

        # Maximum Spacing of Stirrups
        self.permissible_max_spacing= min(300,0.75*self.d)

        #Maximum Shear Stress Possible
        if self.fck==20:
            self.tc_max= 2.8             # tc max - Shear STress limit      
        elif self.fck==25:
            self.tc_max= 3.1
        elif self.fck==30:
            self.tc_max= 3.5
        elif self.fck==35:
            self.tc_max= 3.7
        elif self.fck==40:
            self.tc_max= 4
        else:
            self.tc_max= 4

        #Maximum Shear Stress Possible
        bond_stress= [1.92,2.24,2.4,2.72,3.04]
        self.bond_stress_pd= pd.DataFrame(bond_stress, columns=["Deformed Bar"], index=[20,25,30,35,40] )

    def mulim_ast_calculation(self,Mu,BMC,BML,BMR):
        """This function of :class:`PyRCD.RCbeam.rcb` objects calculates the reinforcement area required. By default, it is set as per Indian Standard IS456:2000. It can be canged as per the guideline user aim to follow. 

        :param: None

        :Note: Calculation for determination of moment capacity and steel area can be change as per user requirement. Avoid changing variable name `self.Ast`.
        """
        fy= self.fy
        fc= self.fck
        b= self.b
        d= self.d

        if fy==250:
            c1= 0.149
            x_d = 0.53*d              # xu max / d
            
        elif fy==415:
            c1= 0.138
            x_d = 0.48*d
        
        elif fy==500:
            c1= 0.133
            x_d = 0.46*d     
        else:
            x_d = np.round((0.0035/((0.87*fy/self.Es)+0.0055)),2)
            c1= (0.36*x_d*(1-(0.42*x_d)))
        
        Ast= np.array([])
  
        self.Mu_lim= c1 * fc * b * d * d

        aa= -(0.87*fy*fy)/(fc*b)
        bb= 0.87*fy*d

        cc= BMC*pow(10,6)
        
        if BML !=0:
            cl= BML*pow(10,6)

        if BMR !=0:
            cr= BMR*pow(10,6)

        if self.Mu_lim > abs(Mu):
            
            ast_center = min(abs(np.roots([aa,bb,cc])))
            
            if BML!=0:
                ast_left = min(abs(np.roots([aa,bb,cl])))
            else:
                ast_left= self.ast_min

            if BMR !=0:
                ast_right= min(abs(np.roots([aa,bb,cr])))
            else:
                ast_right= self.ast_min
            
            self.Ast=np.array([ast_center, ast_left, ast_right ])
                    

            for idx, x in np.ndenumerate(Ast):
                if abs(x)<self.ast_min:
                    if x_d<0:
                        Ast[idx]= -self.ast_min
                    else:
                        Ast[idx]= self.ast_min
            self.skip_status= False
        else: 
            self.Ast= np.array([10000, 10000, 10000])
            self.skip_status= True
        

    def ld_calculation(self):
        """This function of :class:`PyRCD.RCbeam.rcb` objects calculates the anchorage / development length of top and bottom bars in the design and optimization of RC beam. By default, it is set as per Indian Standard IS456:2000. It can be canged as per the guideline user aim to follow. 

        :param: None

        :Note: Calculation for determination of development length can be changed as per user requirement. Avoid changing the variable names.
        """
        rebar_top= self.rebar_detail.iloc[1:,5:12].to_numpy()
        rebar_bottom= self.rebar_detail.iloc[0,5:12].to_numpy()
        
        max_dia_bottom= rebar_bottom[6]
        
        if self.left_end_continous== False:
            max_dia_left_top= rebar_top[0,6]
            if self.fck >35:
                fck= 40
            else:
                fck= self.fck

            tbd= self.bond_stress_pd.at[fck,'Deformed Bar']

            self.Ldlc= (0.87*self.fy*max_dia_left_top/(4*tbd))          # Development length of top left bar
            
            self.Ldb= (0.87*self.fy*max_dia_bottom/(5*tbd))
        else:
            self.Ldlc= self.left_support_size/2
            self.Ldb= self.left_support_size/2

        if self.right_end_continous== False:
            max_dia_right_top= rebar_top[1,6]
            if self.fck >35:
                fck= 40
            else:
                fck= self.fck

            tbd= self.bond_stress_pd.at[fck,'Deformed Bar']

            self.Ldrc= (0.87*self.fy*max_dia_right_top/(4*tbd))         # Development length of top right bar
            self.Ldb= (0.87*self.fy*max_dia_bottom/(5*tbd))
        else:
            self.Ldrc= self.right_support_size/2
            self.Ldb= self.right_support_size/2
 

    def rebar_config(self):
        """This function of :class:`PyRCD.RCbeam.rcb` objects initialized reinforcement bars for the design and optimization of reinforced concrete beam seperatly for tension and shear forces. By default, it is set as per Indian Market. It can be canged as per the guideline user. 

        :param: None
        :Note: Avoid changing the variable names.
        """
        rebar_size= [10,12,16,20,25,32]             # Diameter of rebars as per Indian Market 

        stirrup_bar_size= [8,10,12]                 # Diameter of stirrups bars as per Indian Market 

        stirrup_legs= [1,2,3,4]                     # Stirrups legs possible as per Indian Market 




        # Main Rebar Detail--------------DO NOT CHANGE---------------

        rebar_np= np.zeros((1, 4*len(rebar_size)))
        total_rebar_list= []
        kk=0
        for i in rebar_size:
            for j in range (1,5):
                rebar_np[0,kk]= np.pi*i*i*j/4
                kk= kk+1
                total_rebar_list.append(str(i)+"-"+str(j))

        self.rebar_pd= pd.DataFrame(data= rebar_np,
                            columns=total_rebar_list)
        self.rebars_list= total_rebar_list
        self.rebar_size= rebar_size




        # Bar for stirrups-----------------DO NOT CHANGE--------------------
        stirrup_np= np.zeros((len(stirrup_bar_size)*len(stirrup_legs),3))
        kk=0
        for i in stirrup_bar_size:
            for j in stirrup_legs:
                stirrup_np[kk,0]= np.pi*i*i*j/4
                stirrup_np[kk,1]= i
                stirrup_np[kk,2]= j
                kk= kk+1
        stirrup_pd= pd.DataFrame(data=stirrup_np, columns= ["Area", "Dia", "Leg"] )
        stirrup_pd= stirrup_pd.sort_values(by=['Area'], ignore_index= True)



        self.reb_list= stirrup_pd["Area"].to_list()
        self.rebars_dia= stirrup_pd["Dia"].to_list()
        self.rebar_legs= stirrup_pd["Leg"].to_list()

        List_of_N_1_str = list(itr.combinations(self.reb_list, 1))
        List_of_N_2_str = list(itr.combinations(self.reb_list, 2))   
        self.List_of_N_str= List_of_N_1_str + List_of_N_2_str


    def constructability(self):
        """This function of :class:`PyRCD.RCbeam.rcb` objects initialized constructability parameter for the design and optimization of reinforced concrete beam. By default, it is set as per Indian Market. It can be canged as per the guideline user. 

        :param: None

        :Note: Avoid changing the variable names.
        """

        # --------------DO NOT CHANGE NAME OF VARIABLES---------------
        self.min_space_between_rebar= max(self.nominal_size_aggregate, max(self.rebar_size)) + 5 
        self.min_space_between_stirrups= 70 
        self.two_top_coner_bar_must_be_continous= True

        self.nominal_size_aggregate= 20

        # Limit on Maximum Number of Rebar based on total area required in order to avoid only large diameter
        ast=self.Ast.copy()
        self.max_bars=[]
        for i in ast:
            if i <800:
                self.max_bars.append(5)             # max bar is 6
            
            if i >800 and i <1500:
                self.max_bars.append(8)              # max bar is 8

            if i >1500 and i <2000:
                self.max_bars.append(10)            # max bar is 10

            if i >2000 and i <3000:
                self.max_bars.append(12)            # max bar is 12

            if i >3000 and i <4000:
                self.max_bars.append(16)            # max bar is 16

            if i >4000 and i <6000:                 # max bar is 20
                self.max_bars.append(20)

            if i >6000:                             # max bar is 30
                self.max_bars.append(32)

        # Limit on Maximum and Minimum Size of Rebar based on total area required in order to avoid only large diameter

        #------ CHANGE TRUE to FALSE, if no size limit is there on rebars on beam       
        self.max_size_not_allowed = True
        self.max_size_not_allowed_pd= pd.DataFrame({"Area": [3000,1500], "Max Size Not Allowed": [32,25]})

        self.min_size_not_allowed_in_rebar= True
        self.min_size_not_allowed_in_rebar_size= 10


    def __rebar_construct(self,record_best_fitness,solutions,optimized_area,list_bars, max_bars, ast,common= None):

        b= self.b
        co= self.cover

        rebars_list= self.rebars_list.copy()
        final_fitness= []
        final_index= []

        final_bar1= []
        final_bar2=[]
        final_bar3=[]

        final_num_of_bar1= []
        final_num_of_bar2=[]
        final_num_of_bar3=[]
        min_space= []
        Total_Bars= []
        min_spacing= self.min_space_between_rebar
       
        ib= [ ibb  for ibb in range (0,len(rebars_list)+1,4)]

        for i, x in enumerate(record_best_fitness):
            if x < 700 and (list_bars[i] <= max_bars):
                final_fitness.append(x)
                final_index.append(i)


        final_sol=[solutions[i] for i in final_index]    
        final_optimized_area = [optimized_area[i] for i in final_index]

        pop_index= []

        for i,x in enumerate(final_sol):
                
            if len(x) ==1:  
                status= 1  

                A1 = x[0]
                bar1_index = rebars_list.index(A1)
                op11= int(bar1_index/4)           #helping find op12
                op12= 1+bar1_index-(int(bar1_index/4)*4)

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar1_index <ib[ibb]:
                        bar1= self.rebar_size[ibb-1]

                max_dia= bar1
                min_dia= bar1

                spacing= (b - (2*co)) / (op12)

                # if spacing< min_spacing:
                #     pop_index.append(i) 
                #     status= 0 

                if op12 ==1:
                    if status ==1:
                        pop_index.append(i)
                        status= 0

                final_bar1.append(bar1)
                final_bar2.append(0)
                final_bar3.append(0)

                final_num_of_bar1.append(op12)
                final_num_of_bar2.append(0)
                final_num_of_bar3.append(0)

                totalbars= op12

                if self.max_size_not_allowed == True:
                    for kkk in range (len(self.max_size_not_allowed_pd)):
                        if ast < self.max_size_not_allowed_pd.iat[kkk,0]:
                                if bar1 == self.max_size_not_allowed_pd.iat[kkk,1]:
                                    if status== 1:
                                        pop_index.append(i)
                                        status= 0                       

            # For 2 different bars combo
            if len(x) ==2:
                status= 1

                A1 = x[0]
                A2= x[1]
                bar1_index = rebars_list.index(A1)
                bar2_index = rebars_list.index(A2)
                op11= int(bar1_index/4)           #helping find op12
                op12= 1+bar1_index-(int(bar1_index/4)*4)

                op21= int(bar2_index/4)           #helping find op12
                op22= 1+bar2_index-(int(bar2_index/4)*4)

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar1_index <ib[ibb]:
                        bar1= self.rebar_size[ibb-1]

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar2_index <ib[ibb]:
                        bar2= self.rebar_size[ibb-1]

                max_dia= max (bar1, bar2)
                min_dia= min (bar1, bar2)

                spacing= (b - (2*co))/ (op12 + op22)

                if bar1==bar2:
                    no_bars= op12+op22
                    s= str(bar1)+"-"+str(no_bars)
                    final_sol[i]= s.split(" ")

                    final_bar1.append(bar1)
                    final_bar2.append(0)
                    final_bar3.append(0)

                    final_num_of_bar1.append(no_bars)
                    final_num_of_bar2.append(0)
                    final_num_of_bar3.append(0)

                if bar1!=bar2:
                    final_bar1.append(bar1)
                    final_bar2.append(bar2)
                    final_bar3.append(0)

                    final_num_of_bar1.append(op12)
                    final_num_of_bar2.append(op22)
                    final_num_of_bar3.append(0)

                    if (op12%2 !=0) and (op22%2 !=0):
                            if status== 1:
                                pop_index.append(i) 
                                status= 0

                # if spacing< min_spacing:
                #     pop_index.append(i) 
                #     status= 0

                if op12 ==1 and op22==1:
                    if bar1 != bar2:
                        if status== 1:
                            pop_index.append(i) 
                            status= 0


                totalbars= op12+op22

                if self.max_size_not_allowed == True:
                    for kkk in range (len(self.max_size_not_allowed_pd)):
                        if ast < self.max_size_not_allowed_pd.iat[kkk,0]:
                            for sss in [bar1,bar2]:
                                if sss == self.max_size_not_allowed_pd.iat[kkk,1]:
                                    if status== 1:
                                        pop_index.append(i)
                                        status= 0                       

            # For 3 different bars combo
            if len(x) ==3:
                status= 1

                A1 = x[0]
                A2= x[1]
                A3= x[2]
                bar1_index = rebars_list.index(A1)
                bar2_index = rebars_list.index(A2)
                bar3_index = rebars_list.index(A3)
                op11= int(bar1_index/4)           #helping find op12
                op12= 1+bar1_index-(int(bar1_index/4)*4)

                op21= int(bar2_index/4)           #helping find op22
                op22= 1+bar2_index-(int(bar2_index/4)*4)

                op31= int(bar3_index/4)           #helping find op32
                op32= 1+bar3_index-(int(bar3_index/4)*4)

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar1_index <ib[ibb]:
                        bar1= self.rebar_size[ibb-1]

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar2_index <ib[ibb]:
                        bar2= self.rebar_size[ibb-1]

                for ibb in range (1,len(ib)):
                    if ib[ibb-1]<= bar3_index <ib[ibb]:
                        bar3= self.rebar_size[ibb-1]

                max_dia= max (bar1, bar2, bar3)
                min_dia= min (bar1, bar2, bar3)

                spacing= (b - (2*co))/ (op12 + op22 + op32)

                if bar1==bar2 and bar1!=bar3:
                    no_bars= op12+op22
                    s= str(bar1)+"-"+str(no_bars)+ " " + str(bar3)+"-"+str(op32)
                    final_sol[i]= s.split(" ")

                    final_bar1.append(bar1)
                    final_bar2.append(bar3)
                    final_bar3.append(0)

                    final_num_of_bar1.append(no_bars)
                    final_num_of_bar2.append(op32)
                    final_num_of_bar3.append(0)
                    op121= op12+op22

                    if (op121%2 !=0) and (op32%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0                    

                if bar1==bar3 and bar1!=bar2:
                    no_bars= op12+op32
                    s= str(bar1)+"-"+str(no_bars)+ " " + str(bar2)+"-"+str(op22)
                    final_sol[i]= s.split(" ")

                    final_bar1.append(bar1)
                    final_bar2.append(bar2)
                    final_bar3.append(0)

                    final_num_of_bar1.append(no_bars)
                    final_num_of_bar2.append(op22)
                    final_num_of_bar3.append(0)                
                    op121= op12+op32

                    if (op121%2 !=0) and (op22%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0 

                if bar2==bar3 and bar1!=bar2:
                    no_bars= op22+op32
                    s= str(bar1)+"-"+str(op12)+ " " +  str(bar2)+"-"+ str(no_bars)
                    final_sol[i]= s.split(" ")

                    final_bar1.append(bar1)
                    final_bar2.append(bar2)
                    final_bar3.append(0)

                    final_num_of_bar1.append(op12)
                    final_num_of_bar2.append(no_bars)
                    final_num_of_bar3.append(0)  
                    op221= op22+op32

                    if (op221%2 !=0) and (op12%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0

                if bar2==bar3 and bar1==bar2:
                    no_bars= op12+op22+op32
                    s= str(bar1)+"-"+str(no_bars)
                    final_sol[i]= s.split(" ")

                    final_bar1.append(bar1)
                    final_bar2.append(0)
                    final_bar3.append(0)

                    final_num_of_bar1.append(no_bars)
                    final_num_of_bar2.append(0)
                    final_num_of_bar3.append(0) 

                if bar1!=bar2 and bar1!=bar3 and bar2!=bar3:
                    final_bar1.append(bar1)
                    final_bar2.append(bar2)
                    final_bar3.append(bar3)

                    final_num_of_bar1.append(op12)
                    final_num_of_bar2.append(op22)
                    final_num_of_bar3.append(op32) 

                    if (op12%2 !=0) and (op22%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0

                    if (op12%2 !=0) and (op32%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0

                    if (op32%2 !=0) and (op22%2 !=0):
                        if status== 1:
                            pop_index.append(i) 
                            status= 0

                # if spacing< min_spacing:
                #     pop_index.append(i) 
                #     status= 0


                # min_space.append(min_spacing)
                totalbars= op12+op22+op32

                if (op12%2 !=0) and (op22%2 !=0) and (op32%2 !=0):
                        if (op12%2 !=0) and (op22%2 !=0) and (op32%2 !=0):
                            if status== 1:
                                pop_index.append(i) 
                                status= 0


                if self.max_size_not_allowed == True:
                        for kkk in range (len(self.max_size_not_allowed_pd)):
                            if ast < self.max_size_not_allowed_pd.iat[kkk,0]:
                                for sss in [bar1,bar2,bar3]:
                                    if sss == self.max_size_not_allowed_pd.iat[kkk,1]:
                                        if status== 1:
                                            pop_index.append(i)
                                            status= 0
                                

            if self.min_size_not_allowed_in_rebar== True:
                if min_dia == self.min_size_not_allowed_in_rebar_size:
                    if status== 1:
                        pop_index.append(i)
                        status= 0

            Total_Bars.append(totalbars) 

        for eleminate in sorted(pop_index, reverse = True):
            del final_index[eleminate]
            del final_fitness[eleminate]
            del final_sol[eleminate]
            del final_optimized_area[eleminate] 
            del final_bar1[eleminate] 
            del final_bar2[eleminate] 
            del final_bar3[eleminate] 
            del final_num_of_bar1[eleminate] 
            del final_num_of_bar2[eleminate] 
            del final_num_of_bar3[eleminate] 
            del Total_Bars[eleminate] 

        required_area= [ast for i in range (len(final_sol))]

        
        Final_optimized_rebars=  pd.DataFrame({'Bar_Combination': final_sol, 'Total_Area (mm2)': final_optimized_area, 'Total_Bars': Total_Bars, 'Bar1 (mm)': final_bar1, 'Number of bar1':final_num_of_bar1, 'Bar2 (mm)': final_bar2, 'Number of bar2':final_num_of_bar2, 'Bar3 (mm)': final_bar3, 'Number of bar3':final_num_of_bar3} ) 

        if Final_optimized_rebars.empty:
            print ("FAILURE")
            pass

        Final_optimized_rebars.insert(loc = 2, column = 'Ast Required (mm2)',
                value = required_area)
        
        Final_optimized_rebars.insert(loc = 3, column = 'Difference',
                value = (Final_optimized_rebars["Total_Area (mm2)"]- Final_optimized_rebars["Ast Required (mm2)"]))
        
        delete_duplicate=[]
        df= Final_optimized_rebars.copy()
        for i in range (len(df.index)-1):
            for j in range (i+1, len(df.index)):
                if (df.iloc[i,5]== df.iloc[j,5]) and (df.iloc[i,6]== df.iloc[j,6]):
                    if (df.iloc[i,7]== df.iloc[j,7]) and (df.iloc[i,8]== df.iloc[j,8]):
                        if (df.iloc[i,9]== df.iloc[j,9]) and (df.iloc[i,10]== df.iloc[j,10]):
                            delete_duplicate.append(j)
        df.drop(delete_duplicate, inplace = True)
        df.reset_index(inplace=True, drop= True)

        df= df.round({"Difference":4})
        
        if common== None:
            arr= np.argwhere(df[['Difference']].values == (df[['Difference']].values.min()))
            DesignCost_rebar1= df.loc[arr[:,0]]
        else:
            arrr= np.argwhere(df[['Bar1 (mm)']].values == common)
            DCR= df.loc[arrr[:,0]]

            arrr1= np.argwhere(DCR[['Number of bar1']].values >=2)
            DCR= DCR.iloc[arrr1[:,0],:]

            arr= np.argwhere(DCR[['Difference']].values == (DCR[['Difference']].values.min()))
            DesignCost_rebar1= DCR.iloc[arr[:,0],:]

        if len(DesignCost_rebar1.index)>1:
            arr1= np.argwhere((DesignCost_rebar1[['Total_Bars']].values) == (DesignCost_rebar1[['Total_Bars']].values.min()))
            DesignCost_rebar2= DesignCost_rebar1.iloc[arr1[:,0],:]
            Design_Cost_rebar= DesignCost_rebar2.copy()
        else:
            Design_Cost_rebar= DesignCost_rebar1.copy()

        return (Design_Cost_rebar)
    
    def __rebarweightcalculation(self):

        rd= self.rebar_detail.copy()

        rebar= rd.iloc[:,5:].to_numpy()

        for ii in range (3):
            for jj in range (0,6,2):
                if rebar[ii,jj]==rebar[ii,6]:
                    rebar[ii,jj+1]= rebar[ii,jj+1]-2
                    break

        # rd[["Number of bar1"]]= rd[["Number of bar1"]]-2

        l = self.l*1000
        ls= self.left_support_size
        rs= self.right_support_size
        leff= l + ((ls+ rs)/2)

        # bottom_bar_detail= 
        location_list=[]
        length_list= []
        bar_list= []
        development_length=[]

        for j in range(0,7,2):

            if rebar[0,j+1]==0:
                continue

            total_bars= rebar[0,j+1]

            for k in range (1,total_bars+1):
                ld= 0
                if self.left_end_continous== False and self.right_end_continous== False:
                    length= leff- (2*0.1*leff)
                    ld_corner= 2*rebar[0,8]

                if self.left_end_continous== True and self.right_end_continous== True:
                    length= leff- (2*0.15*leff)
                    ld_corner= (ls/2) + (rs/2)

                if self.left_end_continous== True and self.right_end_continous== False:
                    length= leff- (0.1*leff)-(0.15*leff)
                    ld_corner= (ls/2) + rebar[0,8] 

                if self.left_end_continous== False and self.right_end_continous== True:
                    length= leff- (0.1*leff)-(0.15*leff)
                    ld_corner= rebar[0,8] + (rs/2)

                if j ==6:
                    location_list.append("corner")
                    length= l
                    development_length.append(ld_corner)
                else:
                    location_list.append("middle")
                    development_length.append(ld)

                bar_list.append(rebar[0,j])
                length_list.append(length)

        bottom_bar_df_bars= pd.DataFrame({"Location":location_list, "Type": "Bottom", "Bar": bar_list, "Length": length_list, "Ld": development_length })



        for i in range(1,3):
            location_list=[]
            length_list= []
            bar_list= []
            development_length=[]
            type= []
            for j in range(0,7,2):

                if rebar[i,j+1]==0:
                    continue

                total_bars= rebar[i,j+1]

                for k in range (1,total_bars+1):
                    

                    if j ==6:
                        location_list.append("corner")
                        length= l
                    else:
                        location_list.append("middle")
                        length= 0.25*leff
            
                    development_length.append(rebar[i,8])
                    
                    bar_list.append(rebar[i,j])
                    length_list.append(length)

            if i==1:
                top_bar_df_left= pd.DataFrame({"Location":location_list, "Type": "Top Left", "Bar": bar_list, "Length": length_list, "Ld":development_length })    
            else:
                top_bar_df_right= pd.DataFrame({"Location":location_list, "Type": "Top Right", "Bar": bar_list, "Length": length_list, "Ld":development_length})

        top_bar_df= pd.concat((top_bar_df_left,top_bar_df_right )) 
        self.rebar_length_detail= pd.concat((bottom_bar_df_bars,top_bar_df ))    


    def plotting (self,index=None):
        """This function of :class:`PyRCD.RCbeam` objects perform the detailing of beam as the  finalized design of reinforced concrete beam. It produces both 3D and 2D detailing of RC beam for visualization.  

        :param: None
        """
        if self.optimization_status==True:
            if index is None:
                raise Exception("Index is missing. Index parameter from optimization is needed for detailing")
            
            b= self.optimization_result.at[index,"Solution"][0]
            D= self.optimization_result.at[index,"Solution"][1]+ self.cover
            rd= self.rd_list[index].copy()
            sd= self.sd_list[index].copy()
            
        else:    
            b= self.b
            D= self.d+ self.cover
            rd= self.rebar_detail.copy()
            sd= self.shear_detail.copy()

        bottom_bars_pd = rd.iloc[0,:].to_frame().T  
        top_bars= rd.iloc[1:,5:]
        top_bars_np= top_bars.iloc[:,0:7].to_numpy()  

        if self.plotting_status == False:
            raise Exception ("Detailing requires designing. Please perform design or optimization")


        l= self.l*1000

        cover= self.cover
        left_support_size= self.left_support_size
        right_support_size= self.right_support_size
        left_end_continous= self.left_end_continous
        right_end_continous= self.right_end_continous
        # side_bar= self.side_bar
        # side_bar_size=  self.side_bar_size
        col_cover= 50                   # column cover
        col_bar= 16                     # column bar at edge
        
                               # for 2D plotting
                               # for 2D plotting


        if not isinstance (left_support_size, (int,float)):
            raise Exception ("Type of 'left_support_size' must be a int/float representing the width of the left support")
        ls= left_support_size

        xl= [0,0,-ls,-ls,0,0,-ls,-ls]
        yl= [0,b,b,0,0,b,b,0]
        zl= [-D,-D,-D,-D,D,D,D,D]

        if not isinstance (right_support_size, (int,float)):
            raise Exception ("Type of 'right_support_size' must be a int/float representing the width of the right support")
        rs= right_support_size


        xr= [l,l,l+rs,l+rs,l,l,l+rs,l+rs]
        yr= [0,b,b,0,0,b,b,0]
        zr= [-D,-D,-D,-D,D,D,D,D]

        x_2d_1= [-ls, l+rs]
        y_2d_1= [  D,    D]

        x_2d_2= [-ls, -ls,  0, 0, l,  l, l+rs, l+rs]
        y_2d_2= [  0,  -D, -D, 0, 0, -D,   -D,    0]


        leff= l + ((ls+ rs)/2)

        if left_end_continous==False:
            xs= 0
            x_2d_3= [-ls, -ls]
            y_2d_3= [  0,   D]
            left_break_line= False
        else:
            xs= -4*ls
            x_2d_3= [-ls, -ls*3, -ls*3, -ls]
            y_2d_3= [  0,     0,     D,   D]
            left_break_line= True

        if right_end_continous==False:
            xe= l
            x_2d_4= [l+rs, l+rs]
            y_2d_4= [  0,   D]
            right_break_line= False
        else:
            xe= l+ (4*rs)
            x_2d_4= [l+rs, l+(3*rs), l+(3*rs), l+rs]
            y_2d_4= [  0,         0,        D,    D]
            right_break_line= True



        x= [xs,xs,xe,xe,xs,xs,xe,xe]
        y= [0,b,b,0,0,b,b,0]
        z= [0,0,0,0,D,D,D,D]




        fig = go.Figure(data=[
            go.Mesh3d(
                # 8 vertices of a cube
                x=x,
                y=y,
                z=z,
                colorbar_title='z',
                colorscale=[[0, 'gold'],
                            [0.5, 'gold'],
                            [1, 'gold']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity = np.linspace(0, 1, 12, endpoint=True),
                intensitymode='cell',
                # i, j and k give the vertices of triangles
                i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                flatshading = True,
                opacity=0.1,
                showscale=False
            )
        ])

        # Left suport Mesh 
        fig.add_trace(go.Mesh3d(
                # 8 vertices of a cube
                x=xl,
                y=yl,
                z=zl,
                colorbar_title='z',
                colorscale=[[0, 'gold'],
                            [0.5, 'gold'],
                            [1, 'gold']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity = np.linspace(0, 1, 12, endpoint=True),
                intensitymode='cell',
                # i, j and k give the vertices of triangles
                i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                flatshading = True,
                opacity=0.1,
                showscale=False
            )
        )

        # Right suport Mesh
        fig.add_trace(go.Mesh3d(
                # 8 vertices of a cube
                x=xr,
                y=yr,
                z=zr,
                colorbar_title='z',
                colorscale=[[0, 'gold'],
                            [0.5, 'gold'],
                            [1, 'gold']],
                # Intensity of each vertex, which will be interpolated and color-coded
                intensity = np.linspace(0, 1, 12, endpoint=True),
                intensitymode='cell',
                # i, j and k give the vertices of triangles
                i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                flatshading = True,
                opacity=0.1,
                showscale=False
            )
        )

        fig1= go.Figure()
        fig1.add_trace(go.Scatter(x=x_2d_1, y=y_2d_1, mode= 'lines',
                    line_shape='linear', line=dict(color='black', width=4)))
        fig1.add_trace(go.Scatter(x=x_2d_2, y=y_2d_2, mode= 'lines',
                    line_shape='linear', line=dict(color='black', width=4)))
        fig1.add_trace(go.Scatter(x=x_2d_3, y=y_2d_3, mode= 'lines',
                    line_shape='linear', line=dict(color='black', width=4)))
        fig1.add_trace(go.Scatter(x=x_2d_4, y=y_2d_4, mode= 'lines',
                    line_shape='linear', line=dict(color='black', width=4)))     

        fig1.add_shape(type="rect",
            x0=500, y0=-D, x1=500+2*b, y1=-2*D,
            line=dict(color="black"),
        )

        fig1.add_shape(type="rect",
            x0=l-500, y0=-D, x1=l-500-2*b, y1=-2*D,
            line=dict(color="black"),
        )

        fig1.add_shape(type="rect",
            x0=(l/2)-(b), y0=-D, x1=(l/2)+(b), y1=-2*D,
            line=dict(color="black"),
        )  

    #--------------Bottom Bars Plotting-------------------

        if left_end_continous== False and right_end_continous== False:
            st= 0   #-ls/2
            en= l   #+(rs/2)

        if left_end_continous== True and right_end_continous== True:
            st= 0- (4*ls)
            en= l+(4*ls)

        if left_end_continous== True and right_end_continous== False:
            st= 0- (4*ls)
            en= l   #+(rs/2)

        if left_end_continous== False and right_end_continous== True:
            st= 0   #-ls/2
            en= l+(4*ls)

        x1= [st, en]
        y1= [cover, cover]
        z1= [cover, cover]

        l1= en-st

        x3= [st, en]
        y3= [(b-cover), (b-cover)]
        z3= [cover, cover]

        rebar= rd.iloc[:,4:14].to_numpy()

        colour = self.__rebar_colour(rebar[ 0, 7])
        colorscale = [[0, colour],
                [1, colour]]
        
        x_cyl, y_cyl, z_cyl = self.__cylinder(x1[0], y1[0], z1[0], (rebar[ 0, 7]/2), l1)

        fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

        x_cyl, y_cyl, z_cyl = self.__cylinder(x3[0], y3[0], z3[0], (rebar[ 0, 7]/2), l1)

        fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

        fig1.add_trace(go.Scatter(x=x1, y=z1, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2))) 
        
        # plotting marker for bars
        xx_bar_l= [500+2*cover, 500+2*b-2*cover]
        zz_bar_l= [-2*D+cover, -2*D+cover ]
        
        fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
                        marker=dict(size=[rebar[ 0, 7],rebar[ 0, 7]],
                                color=colour)))
        
        xx_bar_r= [l-500-2*cover, l-500-2*b+2*cover]
        fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
                    marker=dict(size=[rebar[ 0, 7],rebar[ 0, 7]],
                                color=[colour,colour])))

        xx_bar_c= [(l/2)-(b)+2*cover, (l/2)+(b)-2*cover]
        fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_l, mode= 'markers',
                    marker=dict(size=[rebar[ 0, 7],rebar[ 0, 7]],
                                color=[colour,colour])))

        #NEW-----------------------Middile Bottom Rebar Detailing
        x_end = xx_bar_c
        y_end = zz_bar_l
        x_start = [(l/2)-(1.4*b), (l/2)+(1.4*b)]
        y_start = [-1.8*D, -1.8*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=(l/2)-(1.8*b), y=-1.8*D, xref="x", yref="y", text= f'<b> {rebar[ 0, 7]}# Bar</b>'  , showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black"), align="center")

        fig1.add_annotation( x=(l/2)+(1.8*b), y=-1.8*D, xref="x", yref="y", text=f'<b>{rebar[ 0, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")


        x_end = xx_bar_l
        y_end = zz_bar_l
        x_start = [(250), (500+ (2.7*b))]
        y_start = [-1.8*D, -1.8*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=250, y=-1.78*D, xref="x", yref="y", text=f'<b>{rebar[ 0, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")

        fig1.add_annotation( x=(500+(2.7*b)), y=-1.78*D, xref="x", yref="y", text=f'<b>{rebar[ 0, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")


        x_end = xx_bar_r
        y_end = zz_bar_l
        x_start = [l-200, l-500-(2.5*b)]
        y_start = [-1.8*D, -1.8*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=l-200 , y=-1.78*D, xref="x", yref="y", text=f'<b>{rebar[ 0, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")

        fig1.add_annotation( x=l-500-(2.9*b), y=-1.78*D, xref="x", yref="y", text=f'<b>{rebar[ 0, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")

        #NEW END-----------------------


        #NEW-----------------------Stirrups Annotations
        x_end = [(l/2)-(b)+2*cover-(rebar[ 0, 7]/2)]
        y_end = [-1.5*D]                                        #zz_bar_l
        x_start = [(l/2)-(1.4*b)]
        y_start = [-1.5*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=(l/2)-(2.2*b), y=-1.5*D, xref="x", yref="y", text=f'<b>{self.shear_detail.iloc[ 0, 1]}# Bar  <br>@ {int(self.shear_detail.iloc[ 2, 3])}mm</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")



        x_end = [500+2*cover -(rebar[ 0, 7]/2)]
        y_end = [-1.5*D]                        #zz_bar_l
        x_start = [(350)]
        y_start = [-1.5*D]
        list_of_all_arrows = []
        
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=200, y=-1.5*D, xref="x", yref="y", text=f'<b>{self.shear_detail.iloc[ 1, 1]}# Bar <br>@ {int(self.shear_detail.iloc[ 0, 3])}mm</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")




        x_end = [l-500-2*cover+ (rebar[ 0, 7]/2)]
        y_end = [-1.5*D]                                    #zz_bar_l
        x_start = [l-350]
        y_start = [-1.5*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=l-100 , y=-1.5*D, xref="x", yref="y", text=f'<b>{self.shear_detail.iloc[ 2, 1]}# Bar <br>@ {int(self.shear_detail.iloc[ 1, 3])}mm</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")



        #NEW END-----------------------


        # Development Length Left support Bottom
        if left_end_continous== False:
            L_ld_left= left_support_size- col_cover - (col_bar/2)- (rebar[ 0, 7])-  (rebar[ 1, 7])   
            cord_ld_left= 0 - L_ld_left
            
            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_left, y1[0], z1[0], (rebar[ 0, 7]/2), L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_left, y3[0], z3[0], (rebar[ 0, 7]/2), L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            ld_remaining_left= rebar[ 0, 9]-L_ld_left
            

            if ld_remaining_left < (D- (2*cover+rebar[ 1, 7]+rebar[ 0, 7])):
                L_ld_left= ld_remaining_left   
                x11= cord_ld_left- (rebar[ 0, 7]/2)
                z11= cover- (rebar[ 0, 7]/2)                    # top bend

                x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y1[0], z11, (rebar[ 0, 7]/2), L_ld_left)

                fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))
            
                x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y3[0], z11, (rebar[ 0, 7]/2), L_ld_left)

                fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

                x2_2d= [st, cord_ld_left, x11 ]
                z2_2d= [cover, cover, z11+ld_remaining_left ]
            else:
                x11= cord_ld_left- (rebar[ 0, 7]/2)
                z11= cover- (rebar[ 0, 7]/2) 
                x2_2d= [st, cord_ld_left, x11 ]
                z2_2d= [cover, cover, z11+ld_remaining_left ]

            fig1.add_trace(go.Scatter(x=x2_2d, y=z2_2d, mode= 'lines', line_shape='linear', line=dict(color='red', width=2)))
            
        # Development Length Right support Bottom
        if right_end_continous== False:
            
            L_ld_right= right_support_size- col_cover - (col_bar/2)- (rebar[ 0, 7])-  (rebar[ 1, 7])    
            cord_ld_right= l

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_right, y1[0], z1[0], (rebar[ 0, 7]/2), L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_right, y3[0], z3[0], (rebar[ 0, 7]/2), L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            ld_remaining_right= rebar[ 0, 9]-L_ld_right

            x22=  L_ld_right
            

            if ld_remaining_right < (D- (2*cover+rebar[ 1, 7]+rebar[ 0, 7])):
    
                x11= cord_ld_right + L_ld_right + (rebar[ 0, 7]/2)
                L_ld_right= ld_remaining_right
                z11= cover- (rebar[ 0, 7]/2)                    # top bend

                x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y1[0], z11, (rebar[ 0, 7]/2), L_ld_right)

                fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))
            
                x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y3[0], z11, (rebar[ 0, 7]/2), L_ld_right)

                fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

                x2_2d= [en, en+x22, x11 ]
                z2_2d= [cover, cover, z11+ld_remaining_right ]
            else:
                x11= cord_ld_right + L_ld_right + (rebar[ 0, 7]/2)
                z11= cover- (rebar[ 0, 7]/2)
                x2_2d= [en, en+x22, x11 ]
                z2_2d= [cover, cover, z11-ld_remaining_right ]

            fig1.add_trace(go.Scatter(x=x2_2d, y=z2_2d, mode= 'lines',
                        line_shape='linear', line=dict(color='red', width=2)))
            
            
        corner_bar= rebar[ 0, 7]
        space= (b- (2*cover))/ (rebar[0,0]- 1)
        total_bars_bottom= rebar[0,0]- 2

        find_bar= rebar[0,7]
        availability= np.where(rebar[0,:6] == find_bar)
        loca= availability[0]  
        rebar[0,loca+1]= rebar[0,loca+1]-2
        

            
        for i in range (1,total_bars_bottom+1):
            
            if left_end_continous==False:
                start= 0.1*leff
            else:
                start= 0.15*leff

            if right_end_continous==False:
                end= 0.1*leff
            else:
                end= 0.15*leff

            l2= (l+(rs/2)-end) -  (-ls/2 + start)

            x2= [(-ls/2 + start), (l+(rs/2)-end)]
            y2= [(cover+(i*space)), (cover+(i*space))]
            z2= [cover, cover]

            if rebar[0,2] !=0:
                if rebar[0,1] !=0:

                    colour = self.__rebar_colour(rebar[ 0, 1])
                    colorscale = [[0, colour],
                            [1, colour]]
                    
                    shift= rebar[ 0, 1] - corner_bar

                    x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] + shift , (rebar[ 0, 1]/2), l2)

                    fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

                    rebar[0,2]= rebar[0,2]-1
                    
                    actual_rebar= rebar[0,1]

                    xx_bar_c= [(l/2)-(b)+2*cover+(i*space*2)]
                    zz_bar_c= [-2*D+cover]
                    fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_c, mode= 'markers',
                    marker=dict(size=[rebar[ 0, 1],rebar[ 0, 1]],
                                color=[colour,colour])))
                    
            if rebar[0,4] !=0:
                if rebar[0,3] !=0:

                    colour = self.__rebar_colour(rebar[ 0, 3])
                    colorscale = [[0, colour],
                            [1, colour]]
                    
                    shift= rebar[ 0, 3] - corner_bar

                    x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] + shift , (rebar[ 0, 3]/2), l2)

                    fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))    

                    rebar[0,4]= rebar[0,4]-1

                    actual_rebar= rebar[0,3]

                    xx_bar_c= [(l/2)-(b)+2*cover+(i*space*2)]
                    zz_bar_c= [-2*D+cover]
                    fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_c, mode= 'markers',
                    marker=dict(size=[rebar[ 0, 3],rebar[ 0, 3]],
                                color=[colour,colour])))


            if rebar[0,6] !=0:
                if rebar[0,5] !=0:

                    colour = self.__rebar_colour(rebar[ 0, 5])
                    colorscale = [[0, colour],
                            [1, colour]]
                    
                    shift= rebar[ 0, 5] - corner_bar

                    x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] + shift , (rebar[ 0, 5]/2), l2)

                    fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8)) 

                    rebar[0,6]= rebar[0,6]-1
                    actual_rebar= rebar[0,5]

                    xx_bar_c= [(l/2)-(b)+2*cover+(i*space*2)]
                    zz_bar_c= [-2*D+cover]
                    fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_c, mode= 'markers',
                    marker=dict(size=[rebar[ 0, 5],rebar[ 0, 5]],
                                color=[colour,colour])))


            # x_end = xx_bar_c
            # y_end = zz_bar_c
            # x_start = [(l/2)-(1.4*b), (l/2)+(1.4*b)]
            # y_start = [-1.8*D, -1.8*D]
            # list_of_all_arrows = []
            # for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            #     fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
            #                     showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            #     # list_of_all_arrows.append(arrow)
            # fig1.add_annotation( x=(l/2)-(1.4*b), y=-1.8*D, xref="x", yref="y", text=f"{actual_rebar}# Bar", showarrow=False, font=dict( family="Courier New, monospace", size=16, color="black" ), align="center")

            # fig1.add_annotation( x=(l/2)+(1.4*b), y=-1.8*D, xref="x", yref="y", text=f"{rebar[ 0, 7]}# Bar", showarrow=False, font=dict( family="Courier New, monospace", size=16, color="black" ), align="center")
       
    #------------------END ------------------------


    #--------------Top Bars Plotting-------------------
        if left_end_continous== False and right_end_continous== False:
            st= 0   #-ls+75
            en= l   #(l+(rs)-75)

        if left_end_continous== True and right_end_continous== True:
            st= 0- (4*ls)
            en= l+(4*ls)

        if left_end_continous== True and right_end_continous== False:
            st= 0- (4*ls)
            en= l   #(l+(rs)-75)

        if left_end_continous== False and right_end_continous== True:
            st= 0   #-ls+75
            en= l+(4*ls)

        x1= [st, en]
        y1= [cover, cover]
        z1= [D- cover, D- cover]

        l1= en-st

        x3= [st, en]
        y3= [(b-cover), (b-cover)]
        z3= [D- cover, D- cover]
        rebar= rd.iloc[:,4:14].to_numpy()
        
        colour = self.__rebar_colour(rebar[1, 7])
        colorscale = [[0, colour],
                [1, colour]]
        
        x_cyl, y_cyl, z_cyl = self.__cylinder(x1[0], y1[0], z1[0], (rebar[ 1, 7]/2), l1)

        fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

        x_cyl, y_cyl, z_cyl = self.__cylinder(x3[0], y3[0], z3[0], (rebar[ 1, 7]/2), l1)

        fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

        fig1.add_trace(go.Scatter(x=x1, y=z1, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2))) 


        # plotting marker for bars
        xx_bar_l= [500+2*cover, 500+2*b-2*cover]
        zz_bar_l= [-D-cover, -D-cover ]
        
        fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
                        marker=dict(size=[rebar[ 1, 7],rebar[ 1, 7]],
                                color=colour)))
        
        xx_bar_r= [l-500-2*cover, l-500-2*b+2*cover]
        fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
                    marker=dict(size=[rebar[ 1, 7],rebar[ 1, 7]],
                                color=[colour,colour])))

        xx_bar_c= [(l/2)-(b)+2*cover, (l/2)+(b)-2*cover]
        fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_l, mode= 'markers',
                    marker=dict(size=[rebar[ 1, 7],rebar[ 1, 7]],
                                color=[colour,colour])))


        x_end = xx_bar_c
        y_end = zz_bar_l
        x_start = [(l/2), (l/2)]
        y_start = [-0.8*D, -0.8*D]
        list_of_all_arrows = []
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=(l/2), y=-0.75*D, xref="x", yref="y", text=f'<b> {rebar[ 1, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="center")

        x_end = xx_bar_l
        y_end = zz_bar_l
        x_start = [(250), (250)]
        y_start = [-1.2*D, -1.2*D]
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        fig1.add_annotation( x=(200), y=-1.25*D, xref="x", yref="y", text=f'<b>{rebar[ 1, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="left")

        x_end = xx_bar_r
        y_end = zz_bar_l
        x_start = [l-250, l-250]
        y_start = [-1.2*D, -1.2*D]
        for x0x,y0y,x1x,y1y in zip(x_end, y_end, x_start, y_start):
            fig1.add_annotation(dict(x=x0x, y=y0y, xref="x", yref="y", text="",
                            showarrow=True, axref="x", ayref='y', ax=x1x, ay=y1y, arrowhead=3, arrowwidth=1.5, arrowcolor='green',) )
            # list_of_all_arrows.append(arrow)
        # fig1.update_layout(annotations=list_of_all_arrows)
        fig1.add_annotation( x=(l-200), y=-1.25*D, xref="x", yref="y", text=f'<b> {rebar[ 1, 7]}# Bar</b>', showarrow=False, font=dict( family="Courier New, monospace", size=22, color="black" ), align="right")




        # Development Length Right support TOP
        if left_end_continous== False:
            L_ld_left= left_support_size- col_cover - (col_bar/2)- (rebar[ 1, 7])   
            cord_ld_left= 0 - L_ld_left

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_left, y1[0], z1[0], (rebar[ 1, 7]/2), L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_left, y3[0], z3[0], (rebar[ 1, 7]/2), L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            ld_remaining_left= rebar[ 1, 9]-L_ld_left

            L_ld_left= ld_remaining_left   
            x11= cord_ld_left- (rebar[ 1, 7]/2)
            z11= z1[0] + (rebar[ 1, 7]/2)                    # top bend

            x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y1[0], z11, (rebar[ 1, 7]/2), -L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))
        
            x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y3[0], z11, (rebar[ 1, 7]/2), -L_ld_left)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            x2_2d= [st, cord_ld_left, x11 ]
            z2_2d= [D- cover, D- cover, z11-ld_remaining_left ]
            
            fig1.add_trace(go.Scatter(x=x2_2d, y=z2_2d, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))
            

        # Development Length Right support TOP
        if right_end_continous== False:
            L_ld_right= right_support_size- col_cover - (col_bar/2)- (rebar[ 2, 7])    
            cord_ld_right= l

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_right, y1[0], z1[0], (rebar[ 2, 7]/2), L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            x_cyl, y_cyl, z_cyl = self.__cylinder(cord_ld_right, y3[0], z3[0], (rebar[ 2, 7]/2), L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            ld_remaining_right= rebar[ 2, 9]-L_ld_right

            x22= L_ld_right
    
            x11= cord_ld_right + L_ld_right + (rebar[ 2, 7]/2)
            L_ld_right= ld_remaining_right
            z11= z1[0]+ (rebar[ 2, 7]/2)                    # top bend

            x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y1[0], z11, (rebar[ 2, 7]/2), -L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))
        
            x_cyl, y_cyl, z_cyl = self.__cylinderZ(x11, y3[0], z11, (rebar[ 2, 7]/2), -L_ld_right)

            fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))


            x2_2d= [en, en+x22, x11 ]
            z2_2d= [D-cover, D-cover, z11-ld_remaining_right ]

            fig1.add_trace(go.Scatter(x=x2_2d, y=z2_2d, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))
            


        space_l= (b- (2*cover))/ (rebar[1,0]- 1)
        space_r= (b- (2*cover))/ (rebar[2,0]- 1)
 
        total_bars_top_left= rebar[1,0]- 2
        total_bars_top_right= rebar[2,0]- 2

        find_bar= rebar[1,7]
        availability1= np.where(rebar[1,:6] == find_bar)
        availability2= np.where(rebar[2,:6] == find_bar)
        loca1= availability1[0] 
        loca2= availability2[0] 
        rebar[1,loca1+1]= rebar[1,loca1+1]-2
        rebar[2,loca2+1]= rebar[2,loca2+1]-2

        # rebar[1,2]= rebar[1,2]-2
        # rebar[2,2]= rebar[2,2]-2

        corner_bar= rebar[ 1, 7]

        # top left bars
        for i in range (1,total_bars_top_left+1):
            
            if left_end_continous== False:
                end= 0.25*l
                st= -ls+75
                x2= [(st), (end)]
                y2= [(cover+(i*space_l)), (cover+(i*space_l))]
                z2= [D- cover, D- cover]

            if left_end_continous== True:
                st= 0.25*l
                end= 0- ls - st
                x2= [ st, end]
                y2= [(cover+(i*space_l)), (cover+(i*space_l))]
                z2= [D- cover, D- cover]        

            l2= end-st

            if rebar[1,2] >= rebar[1,4] and  rebar[1,2] >= rebar[1,6]:
                col_no= 2
            if rebar[1,4] > rebar[1,2] and  rebar[1,4] >= rebar[1,6]:
                col_no= 4                  
            if rebar[1,6] > rebar[1,2] and  rebar[1,6] >= rebar[1,4]:
                col_no= 6 

            if rebar[1,col_no] !=0:
                if rebar[1,col_no-1] !=0:

                    colour = self.__rebar_colour(rebar[ 1, col_no-1])
                    colorscale = [[0, colour],
                            [1, colour]]
                    
                    shift= rebar[ 1, col_no-1] - corner_bar

                    x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 1, col_no-1]/2), l2)

                    fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

                    rebar[1,col_no]= rebar[1,col_no]-1

                    xx_bar_l= [500+2*cover+(i*space_l*2)]
                    if rebar[ 1, col_no-1]==12:
                        zz_bar_l= [-D-cover]
                    else:
                        zz_bar_l= [-D-cover-(rebar[ 1, col_no-1]/2)]
                    
                    fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
                                    marker=dict(size=[rebar[ 1, col_no-1]],        
                                            color=colour)))     #,rebar[ 1, 1]
                    continue
                

            # if rebar[1,2] !=0:
            #     if rebar[1,1] !=0:

            #         colour = self.__rebar_colour(rebar[ 1, 1])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 1, 1] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 1, 1]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[1,2]= rebar[1,2]-1

            #         xx_bar_l= [500+2*cover+(i*space_l*2)]
            #         if rebar[ 1, 1]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 1, 1]/2)]
                    
            #         fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
            #                         marker=dict(size=[rebar[ 1, 1]],        
            #                                 color=colour)))     #,rebar[ 1, 1]
            #         continue
                
            # if rebar[1,4] !=0:
            #     if rebar[1,3] !=0:

            #         colour = self.__rebar_colour(rebar[ 1, 3])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 1, 3] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 1, 3]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[1,4]= rebar[1,4]-1

            #         xx_bar_l= [500+2*cover+(i*space_l*2)]
            #         if rebar[ 1, 3]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 1, 3]/2)]
                    
            #         fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
            #                         marker=dict(size=[rebar[ 1, 3]],
            #                                 color=colour)))
            #         continue


            # if rebar[1,6] !=0:
            #     if rebar[1,5] !=0:

            #         colour = self.__rebar_colour(rebar[ 1, 5])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 1, 5] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 1, 5]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[1,6]= rebar[1,6]-1

            #         xx_bar_l= [500+2*cover+(i*space_l*2)]
            #         if rebar[ 1, 5]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 1, 5]/2)]
                    
            #         fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'markers',
            #                         marker=dict(size=[rebar[ 1, 5],],
            #                                 color=colour)))          #rebar[ 1, 6]
            #         continue


        # top right bars
        for i in range (1,total_bars_top_right+1):
            
            if right_end_continous== False:
                start= l-(0.25*l)
                end= l+(rs)-75
                x2= [(start), (end)]
                y2= [(cover+(i*space_r)), (cover+(i*space_r))]
                z2= [D- cover, D- cover]

            if right_end_continous== True:
                start= 0.75*l
                end= start + rs + (2*0.25*l)
                x2= [ start, end]
                y2= [(cover+(i*space_r)), (cover+(i*space_r))]
                z2= [D- cover, D- cover]        
            
            l2= end-start


            if rebar[2,2] >= rebar[2,4] and  rebar[2,2] >= rebar[2,6]:
                col_no= 2
            if rebar[2,4] > rebar[2,2] and  rebar[2,4] >= rebar[2,6]:
                col_no= 4                  
            if rebar[2,6] > rebar[2,2] and  rebar[2,6] >= rebar[2,4]:
                col_no= 6 

            if rebar[2,col_no] !=0:
                if rebar[2,col_no-1] !=0:

                    colour = self.__rebar_colour(rebar[ 2, col_no-1])
                    colorscale = [[0, colour],
                            [1, colour]]
                    
                    shift= rebar[ 2, col_no-1] - corner_bar

                    x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 2, col_no-1]/2), l2)

                    fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

                    rebar[2,col_no]= rebar[2,col_no]-1

                    xx_bar_r= [l-500-2*cover- ((i*space_r*2))]

                    if rebar[ 2, col_no-1]==12:
                        zz_bar_l= [-D-cover]
                    else:
                        zz_bar_l= [-D-cover-(rebar[ 2, col_no-1]/2)]
                    
                    fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
                                    marker=dict(size=[rebar[ 2, col_no-1]],        
                                            color=colour)))     #,rebar[ 1, 1]
                    continue


            # if rebar[2,2] !=0:
            #     if rebar[2,1] !=0:

            #         colour = self.__rebar_colour(rebar[ 2, 1])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 2, 1] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 2, 1]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[2,2]= rebar[2,2]-1


            #         if rebar[ 2, 1]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 2, 1]/2)]  

            #         xx_bar_r= [l-500-2*cover- ((i*space_r*2))]

            #         fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
            #                     marker=dict(size=[rebar[ 2, 1]],
            #                                 color=[colour,colour])))
            #         continue


            # if rebar[2,4] !=0:
            #     if rebar[2,3] !=0:

            #         colour = self.__rebar_colour(rebar[ 2, 3])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 2, 3] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 2, 3]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[2,4]= rebar[2,4]-1

            #         if rebar[ 2, 3]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 2, 3]/2)]

            #         xx_bar_r= [l-500-2*cover- ((i*space_r*2))]

            #         fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
            #                     marker=dict(size=[rebar[ 2, 3]],
            #                                 color=[colour,colour])))
            #         continue

            # if rebar[2,6] !=0:
            #     if rebar[2,5] !=0:

            #         colour = self.__rebar_colour(rebar[ 2, 5])
            #         colorscale = [[0, colour],
            #                 [1, colour]]
                    
            #         shift= rebar[ 2, 5] - corner_bar

            #         x_cyl, y_cyl, z_cyl = self.__cylinder(x2[0], y2[0], z2[0] - shift , (rebar[ 2, 5]/2), l2)

            #         fig.add_trace( go.Surface(x=x_cyl, y=y_cyl, z=z_cyl, colorscale=colorscale, showscale=False, opacity=0.8))

            #         rebar[2,6]= rebar[2,6]-1

            #         if rebar[ 2, 5]==12:
            #             zz_bar_l= [-D-cover]
            #         else:
            #             zz_bar_l= [-D-cover-(rebar[ 2, 5]/2)]

            #         xx_bar_r= [l-500-2*cover- ((i*space_r*2))]

            #         fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'markers',
            #                     marker=dict(size=[rebar[ 2, 5]],
            #                                 color=[colour,colour])))    
            #         continue                
    #------------------END ------------------------

    #------------------Stirrups ------------------------

        # stirrups coordinates
        z_1st= cover- (rebar[ 0, 7]/2)
        z_2nd= cover- (rebar[ 0, 7]/2)
        z_3rd= cover
        z_4th= D-cover
        z_5th= D-cover+(rebar[ 1, 7]/2)
        z_6th= D-cover+(rebar[ 1, 7]/2)
        z_7th= D-cover
        z_8th= cover

        y_1st= cover
        y_2nd= b-cover
        y_3rd= b-cover+(rebar[ 0, 7]/2)
        y_4th= b-cover+(rebar[ 1, 7]/2)
        y_5th= b-cover
        y_6th= cover
        y_7th= cover- (rebar[ 1, 7]/2)
        y_8th= cover- (rebar[ 0, 7]/2)       

        diag= np.sqrt((cover*cover) + (cover*cover))

        bottom_diag= diag - (rebar[ 0, 7]/2)
        top_diag= diag - (rebar[ 1, 7]/2)

        y_diag1= bottom_diag* np.cos(45 * np.pi/180)
        y_diag2= b- (bottom_diag* np.cos(45 * np.pi/180))
        y_diag3= b- top_diag* np.cos(45 * np.pi/180)
        y_diag4= top_diag* np.cos(45 * np.pi/180)

        z_diag1= bottom_diag* np.cos(45 * np.pi/180)
        z_diag2= bottom_diag* np.cos(45 * np.pi/180)
        z_diag3= D- top_diag* np.cos(45 * np.pi/180)
        z_diag4= D- top_diag* np.cos(45 * np.pi/180)


        str_y= [y_diag1, y_1st, y_2nd, y_diag2, y_3rd, y_4th, y_diag3, y_5th, y_6th, y_diag4, y_7th, y_8th, y_diag1]
        str_z= [z_diag1, z_1st, z_2nd, z_diag2, z_3rd, z_4th, z_diag3, z_5th, z_6th, z_diag4, z_7th, z_8th, z_diag1]

        z22_2d= [z_diag1,z_diag3]
        
        # Stirrups 2D plotting 
        xx_bar_l= [500+2*i-7  if i <b/2 else 500+2*i+7 for i in str_y  ]
        zz_bar_l= [-2*D+i-3  if i <D/2 else -2*D+i+3 for i in str_z]
        
        fig1.add_trace(go.Scatter(x=xx_bar_l, y=zz_bar_l, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))
        
        xx_bar_r= [l-500-2*b+2*i-7 if i <b/2 else l-500-2*b+2*i+7  for i in str_y]
        fig1.add_trace(go.Scatter(x=xx_bar_r, y=zz_bar_l, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))

        xx_bar_c= [(l/2)-(b)+2*i-7 if i <b/2 else (l/2)-(b)+2*i+7  for i in str_y]
        fig1.add_trace(go.Scatter(x=xx_bar_c, y=zz_bar_l, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))


    #------------------END ------------------------  

    #------------------Hooks ------------------------

        bottom_bar_diag= (rebar[0,7]/2)* np.cos(45 * np.pi/180)
        top_bar_diag= (rebar[1,7]/2)* np.cos(45 * np.pi/180)

        b1_c_y= cover
        b1_c_z= cover

        b2_c_y= (b-cover)
        b2_c_z= cover

        b3_c_y= (b-cover)
        b3_c_z= D- cover

        b4_c_y= cover
        b4_c_z= D- cover

        hook_list= [] 
        hook_list2= []

        complete_bars= sd["Number of Bars"].sum()
        bar_list=[]

        for kk in range (len(sd)):
            bar_list.append(sd.iat[kk,4])

        deduction_hook=[]

        for i in range (1,complete_bars+1):
            
            if i <= bar_list[0]:
                hook_length= sd.iat[0,6]

            if i > bar_list[0] and (i <=  (bar_list[0]+bar_list[1])):
                hook_length= sd.iat[1,6]


            if i > (bar_list[0]+bar_list[1]):
                hook_length= sd.iat[2,6]

            yz_hook= hook_length* np.cos(45 * np.pi/180)


            yz_array= np.zeros([2,2])
            yz_array2= np.zeros([2,2])
            j= i % 4

            if j ==1:
                yz_array[0,0]= b1_c_y + bottom_bar_diag
                yz_array[0,1]= b1_c_z - bottom_bar_diag
                yz_array[1,0]= yz_array[0,0] + yz_hook
                yz_array[1,1]= yz_array[0,1] + yz_hook
                hook_list.append(yz_array)
                

                yz_array2[0,0]= b1_c_y - bottom_bar_diag
                yz_array2[0,1]= b1_c_z + bottom_bar_diag
                yz_array2[1,0]= yz_array2[0,0] + yz_hook
                yz_array2[1,1]= yz_array2[0,1] + yz_hook
                hook_list2.append(yz_array2)
                
                hx1= 0
                hx2= -9
                hz1= -5
                hz2= -1
                hxz= [hx1,hx2,hz1,hz2]
                deduction_hook.append(hxz)

            if j ==2:
                yz_array[0,0]= b2_c_y - bottom_bar_diag
                yz_array[0,1]= b2_c_z - bottom_bar_diag
                yz_array[1,0]= yz_array[0,0] - yz_hook
                yz_array[1,1]= yz_array[0,1] + yz_hook
                hook_list.append(yz_array)

                yz_array2[0,0]= b2_c_y + bottom_bar_diag
                yz_array2[0,1]= b2_c_z + bottom_bar_diag
                yz_array2[1,0]= yz_array2[0,0] - yz_hook
                yz_array2[1,1]= yz_array2[0,1] + yz_hook
                hook_list2.append(yz_array2)

                hx1= 1
                hx2= 9
                hz1= -5
                hz2= 0
                hxz= [hx1,hx2,hz1,hz2]
                deduction_hook.append(hxz)

            if j ==3:
                yz_array[0,0]= b3_c_y + top_bar_diag
                yz_array[0,1]= b3_c_z - top_bar_diag
                yz_array[1,0]= yz_array[0,0] - yz_hook
                yz_array[1,1]= yz_array[0,1] - yz_hook
                hook_list.append(yz_array)

                yz_array2[0,0]= b3_c_y - top_bar_diag
                yz_array2[0,1]= b3_c_z + top_bar_diag
                yz_array2[1,0]= yz_array2[0,0] - yz_hook
                yz_array2[1,1]= yz_array2[0,1] - yz_hook
                hook_list2.append(yz_array2)

                hx1= 5
                hx2= 1
                hz1= 0
                hz2= 5
                hxz= [hx1,hx2,hz1,hz2]
                deduction_hook.append(hxz)

            if j ==0:
                yz_array[0,0]= b4_c_y - top_bar_diag
                yz_array[0,1]= b4_c_z - top_bar_diag
                yz_array[1,0]= yz_array[0,0] + yz_hook
                yz_array[1,1]= yz_array[0,1] - yz_hook
                hook_list.append(yz_array)

                yz_array2[0,0]= b4_c_y + top_bar_diag
                yz_array2[0,1]= b4_c_z + top_bar_diag
                yz_array2[1,0]= yz_array2[0,0] + yz_hook
                yz_array2[1,1]= yz_array2[0,1] - yz_hook
                hook_list2.append(yz_array2)

                hx1= -7
                hx2= 1
                hz1= 0
                hz2= 5
                hxz= [hx1,hx2,hz1,hz2]
                deduction_hook.append(hxz)                

        sdd= sd.copy()
        sdd.iloc[1], sdd.iloc[2] = sdd.iloc[2], sdd.iloc[1].copy()

        stirrup_space= 50
        stirrups_count= 0
        for kk in range (len(sdd)):

            total_shear_bars= sdd.iat[kk,4]

            for j in range (total_shear_bars):
                
                str_x= [ stirrup_space for i in range (13)]
                x22_2d= [stirrup_space,stirrup_space]

                fig.add_trace(go.Scatter3d(x=str_x,y=str_y,z=str_z, mode='lines',      
                        line=dict(
                                color="black",  
                                width=(8),
                                ),
                            ))

                hook1= hook_list[stirrups_count]
                hook2= hook_list2[stirrups_count]

                fig.add_trace(go.Scatter3d(x=str_x,y=hook1[:,0],z=hook1[:,1], mode='lines',      
                        line=dict(
                                color="black",  
                                width=(8),
                                ),
                            ))
                
                fig.add_trace(go.Scatter3d(x=str_x,y=hook2[:,0],z=hook2[:,1], mode='lines',      
                        line=dict(
                                color="black",  
                                width=(8),
                                ),
                            ))            


                if (stirrups_count==1):
                    hxz= deduction_hook[stirrups_count]
                    # Stirrups 2D Hook 
                    xx_bar_l_h_1= [500+2*i+hxz[0]  for i in hook1[:,0]]
                    zz_bar_l_h_1= [-2*D+i+hxz[2]  for i in hook1[:,1]]

                    xx_bar_l_h_2= [500+2*i+hxz[1]  for i in hook2[:,0]]
                    zz_bar_l_h_2= [-2*D+i+hxz[3]  for i in hook2[:,1]]                    
                    
                    fig1.add_trace(go.Scatter(x=xx_bar_l_h_1, y=zz_bar_l_h_1, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))

                    fig1.add_trace(go.Scatter(x=xx_bar_l_h_2, y=zz_bar_l_h_2, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))

                    fig1.add_trace(go.Scatter(x=[stirrup_space,stirrup_space], y=[-0.15*D,1.15*D], mode= 'lines',
                                line_shape='linear', line=dict(color='green', width=2, dash= "longdashdot")))

                    fig1.add_annotation( x=stirrup_space, y=-0.2*D, xref="x", yref="y", text="A",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)
                    
                    fig1.add_annotation( x=stirrup_space, y=1.2*D, xref="x", yref="y", text="A",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)
                    
                    fig1.add_annotation( x=500+b, y=-2.2*D, xref="x", yref="y", text="Section A-A",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=30, color="red"), align="center",)
                    
                if (stirrups_count== complete_bars-2):
                    hxz= deduction_hook[stirrups_count]
                    xx_bar_r_h_1= [l-500-2*b+2*i+hxz[0] for i in hook1[:,0]]
                    zz_bar_l_h_1= [-2*D+i+hxz[2]  for i in hook1[:,1]]

                    xx_bar_r_h_2= [l-500-2*b+2*i+hxz[1] for i in hook2[:,0]]
                    zz_bar_l_h_2= [-2*D+i+hxz[3]  for i in hook2[:,1]]

                    fig1.add_trace(go.Scatter(x=xx_bar_r_h_1, y=zz_bar_l_h_1, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))

                    fig1.add_trace(go.Scatter(x=xx_bar_r_h_2, y=zz_bar_l_h_2, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))
                    
                    fig1.add_trace(go.Scatter(x=[stirrup_space,stirrup_space], y=[-0.15*D,1.15*D], mode= 'lines',
                                line_shape='linear', line=dict(color='green', width=2, dash= "longdashdot")))

                    fig1.add_annotation( x=stirrup_space, y=-0.2*D, xref="x", yref="y", text="C",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)
                    
                    fig1.add_annotation( x=stirrup_space, y=1.2*D, xref="x", yref="y", text="C",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)

                    fig1.add_annotation( x=l-500-b, y=-2.2*D, xref="x", yref="y", text="Section C-C",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=30, color="red"), align="center",)
                    

                if (stirrups_count== (int(complete_bars/2))):
                    hxz= deduction_hook[stirrups_count]
                    xx_bar_c_h_1= [(l/2)-(b)+2*i+hxz[0] for i in hook1[:,0]]
                    zz_bar_l_h_1= [-2*D+i+hxz[2] for i in hook1[:,1]]

                    xx_bar_c_h_2= [(l/2)-(b)+2*i+hxz[1] for i in hook2[:,0]]
                    zz_bar_l_h_2= [-2*D+i+hxz[3] for i in hook2[:,1]]

                    fig1.add_trace(go.Scatter(x=xx_bar_c_h_1, y=zz_bar_l_h_1, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))

                    fig1.add_trace(go.Scatter(x=xx_bar_c_h_2, y=zz_bar_l_h_2, mode= 'lines',
                                line_shape='linear', line=dict(color='red', width=2)))
                    
                    fig1.add_trace(go.Scatter(x=[stirrup_space,stirrup_space], y=[-0.15*D,1.15*D], mode= 'lines',
                                line_shape='linear', line=dict(color='green', width=2, dash= "longdashdot")))

                    fig1.add_annotation( x=stirrup_space, y=-0.2*D, xref="x", yref="y", text="B",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)
                    
                    fig1.add_annotation( x=stirrup_space, y=1.2*D, xref="x", yref="y", text="B",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=26, color="red"), align="center",)
                    
                    fig1.add_annotation( x=l/2, y=-2.2*D, xref="x", yref="y", text="Section B-B",showarrow=False,
                                        font=dict( family="Courier New, monospace", size=30, color="red"), align="center",)



                fig1.add_trace(go.Scatter(x=x22_2d, y=z22_2d, mode= 'lines',
                    line_shape='linear', line=dict(color='red', width=2)))
                
                if kk == 0 and j ==(total_shear_bars-1):
                    stirrup_space= stirrup_space + sdd.iat[1,3]
                else:
                    stirrup_space= stirrup_space + sdd.iat[kk,3]

                stirrups_count= stirrups_count + 1




    #------------------END ------------------------ 
    
        fig.update_scenes(aspectmode="data")
        fig.update_layout(
                    scene=dict(
                        xaxis=dict(type="-"),
                        yaxis=dict(type="-"),
                        zaxis=dict(type="-"),))

        fig.update_layout(scene = dict(
                            xaxis_title=' ',
                            yaxis_title=' ',
                            zaxis_title=' '),)

        fig.update_layout(scene = dict(xaxis = dict(showgrid = False,showticklabels = False,showbackground= False),
                                        yaxis = dict(showgrid = False,showticklabels = False,showbackground= False),
                                        zaxis = dict(showgrid = False,showticklabels = False,showbackground= False),
                    ))
        
        camera = dict(
            eye=dict(x=0., y=-2.5, z=3)
                )
        

        fig1.update_layout(
            plot_bgcolor='white'
        )
        fig1.update_xaxes(
            mirror=False,
            showline=False,

        )
        fig1.update_yaxes(
            mirror=False,
            showline=False,

        )




        fig1.update_layout(
                            showlegend=False,
                            xaxis=dict(visible=False),
                            yaxis=dict(visible=False),
                        )



        fig.update_layout(scene_camera=camera)
        fig.update_layout(height= 1000, width=1800)
        fig1.update_layout(height= 1000, width=1800)

        self.detailing3D= fig
        self.detailing2D= fig1


    def __rebar_colour(self,dia):
        if dia== 12:
            colour= '#636EFA'       #blue
        if dia== 16:
            colour=  '#56f507'       #green
        if dia== 20:
            colour= '#eb2f42'       #red
        if dia== 25:
            colour= '#f05bf0'       #pink    
        if dia== 32:
            colour= '#40e6d2'       #crimson
        return colour

    def __cylinder(self,x, y, z, r, dz):
        """Create a cylindrical mesh located at x, y, z, with radius r and height dz"""
        center_z = np.linspace(0, dz, 15)
        theta = np.linspace(0, 2*np.pi, 15)
        theta_grid, x_grid = np.meshgrid(theta, center_z)
        z_grid = r * np.cos(theta_grid) + z
        y_grid = r * np.sin(theta_grid) + y
        x_grid = x_grid + x
        return x_grid, y_grid, z_grid

    def __cylinderZ(self,x, y, z, r, dz):
        """Create a cylindrical mesh located at x, y, z, with radius r and height dz"""
        center_z = np.linspace(0, dz, 15)
        theta = np.linspace(0, 2*np.pi, 15)
        theta_grid, z_grid = np.meshgrid(theta, center_z)
        x_grid = r * np.cos(theta_grid) + x
        y_grid = r * np.sin(theta_grid) + y
        z_grid = z_grid + z
        return x_grid, y_grid, z_grid

    def __objCalculation(self):
        b=self.b
        d= self.d
        co= self.cover
        l =self.l

        self.__rebarweightcalculation()
        rld= self.rebar_length_detail

        shearbar_vol= 0
        for kk in range (len(self.beam_shear_detail)):
                dia= self.beam_shear_detail.iat[kk,1]
                no_bar= self.beam_shear_detail.iat[kk,4]
                cutting_len= self.beam_shear_detail.iat[kk,4]

                shearbar_vol= shearbar_vol + ((np.round((np.pi*dia*dia/4), 4)*no_bar*cutting_len)/1000000000)            #m3

        rebar_vol=  (sum((np.pi*rld.loc[:,"Bar"]*rld.loc[:,"Bar"]/4)*(rld.loc[:,"Length"]+rld.loc[:,"Ld"])))/ 1000000000                  #m3

        total_conc_vol=(b*(d+co)*l/1000000)
        net_conc_vol= (total_conc_vol- ((rebar_vol + shearbar_vol)))

        rebar_weight= (self.den_s* rebar_vol*100)
        shearbar_weight= (self.den_s* shearbar_vol*100)

        total_weight=  rebar_weight+ shearbar_weight + (self.den_c*100* net_conc_vol)                   #in Kg


        total_cost_steel= self.Cost_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   #INR
        total_cost_concrete= self.Cost_concrete*net_conc_vol    #INR
        total_cost_formwork= self.Cost_formwork* ( (b*l/1000) + (2*((d+co)*l/1000)))

        total_CO2_steel= self.CO2_steel* ((self.den_s* rebar_vol*100)+ (self.den_s* shearbar_vol*100))   
        total_CO2_concrete= self.CO2_concrete*(self.den_c*100* net_conc_vol)    
        total_CO2_formwork= self.CO2_formwork * ( (b*l/1000) + (2*((d+co)*l/1000)))*(self.plywood_thickness/1000)*self.plywood_density



        total_cost= total_cost_steel+ total_cost_concrete + total_cost_formwork
        total_CO2= total_CO2_steel+ total_CO2_concrete + total_CO2_formwork

        total_volume= shearbar_vol + rebar_vol + net_conc_vol

        self.optimization_result= pd.DataFrame({"Weight": total_weight, "Volume": total_volume, "Cost": total_cost, "CO2": total_CO2, "Solution": f"{b},{d}", "Conc Vol": net_conc_vol, "Rebar Vol": rebar_vol, "Stirrup Vol": shearbar_vol, "Rebar Weight": rebar_weight, "Stirrup Weight": shearbar_weight}, index= [1]  )
