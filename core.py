import openmc
from mat import  water_mat,  AbstractUO2, Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat, Dy2O3TiO2_mat, B4C_mat, basket_mat, water_mat1, E265_mat, B1_mat, B2_mat, T1_mat, T2_mat
from math import sqrt, pi
from config import *
import random
top_surf=openmc.ZPlane(z0=208.0)
bottom_surf=openmc.ZPlane(z0=-208.0)
top_surf.boundary_type = 'reflective'
bottom_surf.boundary_type = 'reflective'
water_b_surf = openmc.model.HexagonalPrism(edge_length=11*1.275, orientation='y', boundary_type='transmission')
basket_cell = openmc.Cell(fill=basket_mat, region=-water_b_surf )
basket_universe = openmc.Universe(cells=[basket_cell])

def get_TVS_universe(enr, enr_tvegs, rods_inserted=False, tvegs=False, tvegs_5inner_ring=False,  outer_ring=False, outer_ring_enr=False, verbose=True):

     #if outer_ring and not outer_ring_enr:
         #raise Exception('Outer ring enrichment must be set')

    control0_surf=openmc.ZPlane(z0=-177.5)
    #control0_surf.boundary_type = 'reflective'
    control1_surf=openmc.ZPlane(z0=106.3)
    control2_surf=openmc.ZPlane(z0=136.3)

    UO2_mat1 = AbstractUO2(enr).mat
    UO2_mat2=AbstractUO2(enr_tvegs).mat

    if tvegs:
        UO2_mat2 = openmc.Material.mix_materials(
   materials=[
        UO2_mat2,
        Gd2O3_mat,
    ],
    fracs=[0.96, 0.04],
    percent_type='vo')

    else:
        UO2_mat2 = UO2_mat1
    if outer_ring:
        UO2_mat3 = AbstractUO2(outer_ring_enr).mat
    else:
        UO2_mat3=UO2_mat1

    UO2_mat1.volume=pi*(0.3785**2-0.075**2)*355*240
    UO2_mat2.volume = pi * (0.3785 ** 2 - 0.075 ** 2) * 355 *6
    UO2_mat3.volume = pi * (0.3785 ** 2 - 0.075 ** 2) * 355 *66
    tvel_helium_surf=openmc.ZCylinder(r=r1_tvel)
    tvel_fuel_surf=openmc.ZCylinder(r=r2_tvel)
    tvel_helium2_surf=openmc.ZCylinder(r=r3_tvel)
    tvel_cladding_surf=openmc.ZCylinder(r=r4_tvel)
    lower_plug1_surf=openmc.ZCylinder(r=0.2)
    lower_plug2_surf = openmc.ZCylinder(r=0.455)
    upper_plenum1_surf=openmc.ZCylinder(r=0.3865)
    upper_plenum2_surf=openmc.ZCylinder(r=0.455)

    B2_top_surf=openmc.ZPlane(z0=-193.0)
    B1_top_surf=openmc.ZPlane(z0=-181.3)
    lower_plug_top_surf=openmc.ZPlane(z0=-179.0)
    fuel_top_surf=openmc.ZPlane(z0=176.0)
    upper_plenum_top_surf=openmc.ZPlane(z0=198.2)
    T1_top_surf=openmc.ZPlane(z0=202.7)


    central_surf1=openmc.ZCylinder(r=r1_central)
    central_surf2=openmc.ZCylinder(r=r2_central)

    cyz_absorber_surf=openmc.ZCylinder(r=r1_guide)
    cyz_steel_surf=openmc.ZCylinder(r=r2_guide)
    cyz_coolant_surf=openmc.ZCylinder(r=r3_guide)
    cyz_cladding_surf=openmc.ZCylinder(r=r4_guide)

    cyz10_absorber_surf=openmc.ZCylinder(r=r1_guide)
    cyz10_steel_surf=openmc.ZCylinder(r=r2_guide)
    cyz10_coolant_surf=openmc.ZCylinder(r=r3_guide)
    cyz10_cladding_surf=openmc.ZCylinder(r=r4_guide)

    cyz10_absorber0_cell=openmc.Cell(fill=water_mat, region=-cyz10_absorber_surf & +control0_surf & -control1_surf)
    cyz10_absorber1_cell=openmc.Cell(fill=Dy2O3TiO2_mat, region=-cyz10_absorber_surf & +control1_surf & -control2_surf)
    cyz10_absorber2_cell = openmc.Cell(fill=B4C_mat, region=-cyz10_absorber_surf & +control2_surf )
    cyz10_steel_cell = openmc.Cell(fill=steel_mat, region=-cyz10_steel_surf & +cyz10_absorber_surf)
    cyz10_water1_cell = openmc.Cell(fill=water_mat, region=-cyz10_coolant_surf & +cyz10_steel_surf)
    cyz10_cladding_cell = openmc.Cell(fill=E635_mat, region=-cyz10_cladding_surf & +cyz10_coolant_surf)
    cyz10_water2_cell = openmc.Cell(fill=water_mat, region=+cyz10_cladding_surf)
    cyz10_universe = openmc.Universe(cells=[cyz10_absorber0_cell, cyz10_absorber1_cell, cyz10_absorber2_cell, cyz10_steel_cell, cyz10_water1_cell, cyz10_water1_cell, cyz10_cladding_cell, cyz10_water2_cell])
    #water_surf=openmc.model.HexagonalPrism(edge_length=1.275/sqrt(3), orientation='x', boundary_type='transmission')

#TVEL1

    #tvel1_T2_cell=openmc.Cell(fill=T2_mat, region=-tvel_cladding_surf & +T1_top_surf )
    #tvel1_T1_cell=openmc.Cell(fill=T1_mat, region=-tvel_cladding_surf & +upper_plenum_top_surf & -T1_top_surf)

    tvel1_upper_plenum_cell1=openmc.Cell(fill=helium_mat, region= -upper_plenum1_surf & +fuel_top_surf & -T1_top_surf )
    tvel1_upper_plenum_cell2=openmc.Cell(fill=E110_mat, region=+upper_plenum1_surf & -upper_plenum2_surf & +fuel_top_surf & -T1_top_surf )

    tvel1_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel1_fuel_cell=openmc.Cell(fill=UO2_mat1, region=+tvel_helium_surf & -tvel_fuel_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel1_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel1_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel1_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf  )

    tvel1_lower_plug_cell1=openmc.Cell(fill=helium_mat, region=-lower_plug1_surf & +B1_top_surf & -lower_plug_top_surf)
    tvel1_lower_plug_cell2=openmc.Cell(fill=E110_mat, region=+lower_plug1_surf & -lower_plug2_surf & +B1_top_surf & -lower_plug_top_surf)

    tvel1_B1_cell=openmc.Cell(fill=B1_mat, region=-tvel_cladding_surf &+B2_top_surf & -B1_top_surf)
    tvel1_B2_cell=openmc.Cell(fill=B2_mat, region=-tvel_cladding_surf & -B2_top_surf)

    #TVEL2

    tvel2_T2_cell = openmc.Cell(fill=T2_mat, region=-tvel_cladding_surf & +T1_top_surf )
    tvel2_T1_cell = openmc.Cell(fill=T1_mat, region=-tvel_cladding_surf & +upper_plenum_top_surf & -T1_top_surf)

    tvel2_upper_plenum_cell1 = openmc.Cell(fill=helium_mat, region=-upper_plenum1_surf & +fuel_top_surf & -T1_top_surf)
    tvel2_upper_plenum_cell2 = openmc.Cell(fill=E110_mat,
                                            region=+upper_plenum1_surf & -upper_plenum2_surf & +fuel_top_surf & -T1_top_surf)

    tvel2_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel2_fuel_cell=openmc.Cell(fill=UO2_mat2, region=+tvel_helium_surf & -tvel_fuel_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel2_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel2_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel2_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf )

    tvel2_lower_plug_cell1 = openmc.Cell(fill=helium_mat,
                                          region=-lower_plug1_surf & +B1_top_surf & -lower_plug_top_surf)
    tvel2_lower_plug_cell2 = openmc.Cell(fill=E110_mat,
                                          region=+lower_plug1_surf & -lower_plug2_surf & +B1_top_surf & -lower_plug_top_surf)

    tvel2_B1_cell = openmc.Cell(fill=B1_mat, region=-tvel_cladding_surf & +B2_top_surf & -B1_top_surf)
    tvel2_B2_cell = openmc.Cell(fill=B2_mat, region=-tvel_cladding_surf  & -B2_top_surf)

     #TVEL3
    tvel3_T2_cell = openmc.Cell(fill=T2_mat, region=-tvel_cladding_surf & +T1_top_surf )
    tvel3_T1_cell = openmc.Cell(fill=T1_mat, region=-tvel_cladding_surf & +upper_plenum_top_surf & -T1_top_surf)

    tvel3_upper_plenum_cell1 = openmc.Cell(fill=helium_mat, region=-upper_plenum1_surf & +fuel_top_surf & -T1_top_surf)
    tvel3_upper_plenum_cell2 = openmc.Cell(fill=E110_mat,
                                            region=+upper_plenum1_surf & -upper_plenum2_surf & +fuel_top_surf & -T1_top_surf)

    tvel3_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel3_fuel_cell=openmc.Cell(fill=UO2_mat3, region=+tvel_helium_surf & -tvel_fuel_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel3_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel3_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel3_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +lower_plug_top_surf & -fuel_top_surf)
    tvel3_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf )

    tvel3_lower_plug_cell1 = openmc.Cell(fill=helium_mat,
                                          region=-lower_plug1_surf & +B1_top_surf & -lower_plug_top_surf)
    tvel3_lower_plug_cell2 = openmc.Cell(fill=E110_mat,
                                          region=+lower_plug1_surf & -lower_plug2_surf & +B1_top_surf & -lower_plug_top_surf)

    tvel3_B1_cell = openmc.Cell(fill=B1_mat, region=-tvel_cladding_surf & +B2_top_surf & -B1_top_surf)
    tvel3_B2_cell = openmc.Cell(fill=B2_mat, region=-tvel_cladding_surf & -B2_top_surf)

    #tvel4_helium1_cell = openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +bottom_surf & -top_surf)
   # tvel4_fuel_cell = openmc.Cell(fill=UO2_mat4, region=+tvel_helium_surf & -tvel_fuel_surf & +bottom_surf & -top_surf)
    #tvel4_helium2_cell = openmc.Cell(fill=helium_mat,
           #                           region=+tvel_fuel_surf & -tvel_helium2_surf & +bottom_surf & -top_surf)
   # tvel4_cladding_cell = openmc.Cell(fill=E110_mat,
               #                        region=+tvel_helium2_surf & -tvel_cladding_surf & +bottom_surf & -top_surf)
   # tvel4_water_cell = openmc.Cell(fill=water_mat, region=+tvel_cladding_surf & water_surf & +bottom_surf & -top_surf)

    tvel1_universe=openmc.Universe(cells=[tvel1_T2_cell, tvel1_T1_cell, tvel1_upper_plenum_cell1, tvel1_upper_plenum_cell2, tvel1_helium1_cell, tvel1_fuel_cell, tvel1_helium2_cell, tvel1_cladding_cell, tvel1_water_cell, tvel1_lower_plug_cell1, tvel1_lower_plug_cell2, tvel1_B1_cell, tvel1_B2_cell])
    tvel2_universe=openmc.Universe(cells=[tvel2_T2_cell, tvel2_T1_cell, tvel2_upper_plenum_cell1, tvel2_upper_plenum_cell2, tvel2_helium1_cell, tvel2_fuel_cell, tvel2_helium2_cell, tvel2_cladding_cell, tvel2_water_cell, tvel2_lower_plug_cell1, tvel2_lower_plug_cell2, tvel2_B1_cell, tvel2_B2_cell])
    tvel3_universe=openmc.Universe(cells=[tvel3_T2_cell, tvel3_T1_cell, tvel3_upper_plenum_cell1, tvel3_upper_plenum_cell2, tvel3_helium1_cell, tvel3_fuel_cell, tvel3_helium2_cell, tvel3_cladding_cell, tvel3_water_cell, tvel3_lower_plug_cell1, tvel3_lower_plug_cell2, tvel3_B1_cell, tvel3_B2_cell])
    #tvel4_universe = openmc.Universe(cells=[tvel4_helium1_cell, tvel4_fuel_cell, tvel4_helium2_cell, tvel4_cladding_cell, tvel4_water_cell])



    guide_absorber_cell=openmc.Cell(fill=water_mat, region=-cyz_absorber_surf )
    guide_steel_cell=openmc.Cell(fill=E265_mat, region=-cyz_steel_surf & +cyz_absorber_surf )
    guide_water1_cell=openmc.Cell(fill=water_mat, region=-cyz_coolant_surf & +cyz_steel_surf )
    guide_cladding_cell=openmc.Cell(fill=E635_mat, region=-cyz_cladding_surf & +cyz_coolant_surf )
    guide_water2_cell=openmc.Cell(fill=water_mat, region=+cyz_cladding_surf )

    guide_universe=openmc.Universe(cells=[guide_absorber_cell, guide_steel_cell, guide_water1_cell, guide_water1_cell, guide_cladding_cell, guide_water2_cell] )
    if rods_inserted:
     guide_1_universe = cyz10_universe
    else:
     guide_1_universe = guide_universe
    central_cell1=openmc.Cell(fill=water_mat, region=-central_surf1 )
    central_cell2=openmc.Cell(fill=E265_mat, region=+central_surf1 & -central_surf2 )
    central_water_cell=openmc.Cell(fill=water_mat, region= +central_surf2 )

    central_universe=openmc.Universe(cells=[central_cell1, central_cell2, central_water_cell],)

    all_water_cell=openmc.Cell(fill=water_mat)
    water_universe=openmc.Universe(cells=[all_water_cell,])

    lat = openmc.HexLattice()
    lat.center = (0.0, 0.0)
    lat.pitch = [1.275]
    lat.outer = water_universe
    lat.orientation = 'y'

    firts_ring = [tvel3_universe] * 60  # 60
    second_ring = [tvel3_universe] + [tvel1_universe] * 8  # 54
    second_ring *= 6
    if tvegs_5inner_ring:
     third_ring = [tvel1_universe] * 48
    else:
     third_ring = [tvel2_universe] + [tvel1_universe] * 7  # 48
     third_ring *= 6
    four_ring = [tvel1_universe] * 42  # 42
    fife_ring = [tvel1_universe] * 3 + [guide_1_universe] + [tvel1_universe] * 5 + [guide_1_universe] + [
    tvel1_universe] * 5 + [guide_1_universe] + [tvel1_universe] * 5 + [guide_1_universe] + [tvel1_universe] * 5 + [
                  guide_1_universe] + [tvel1_universe] * 5 + [guide_1_universe] + [tvel1_universe] * 2  # 36
    six_ring = [guide_1_universe] + [tvel1_universe] * 4  # 30
    six_ring *= 6
    if tvegs_5inner_ring:
     seven_ring = [tvel1_universe] * 3 + [tvel2_universe]
     seven_ring *= 6
    else:
     seven_ring = [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 4
     seven_ring *= 3
    eight_ring = [tvel1_universe] + [guide_1_universe] + [tvel1_universe]  # 18
    eight_ring *= 6
    nint_ring = [tvel1_universe] * 12  # 12
    ten_ring = [tvel1_universe] * 6
    inner_ring = [central_universe]
    lat.universes = [firts_ring, second_ring, third_ring, four_ring, fife_ring, six_ring, seven_ring, eight_ring, nint_ring, ten_ring, inner_ring]
    #outer_surf=openmc.model.HexagonalPrism(edge_length=11.7*lat.pitch[0], orientation='y', boundary_type='reflective')
    outer_surf = openmc.model.HexagonalPrism(edge_length=13.556, orientation='y',
                                              boundary_type='reflective')
    #outer_surf=openmc.ZCylinder(r=50.0, boundary_type='reflective')
    TVS_cell = openmc.Cell(fill=lat, region=-outer_surf & -top_surf & +bottom_surf )
    #TVS_universe=openmc.Universe(cells=[TVS_cell])
    if verbose:
        print(lat)
    return TVS_cell, list(set((UO2_mat1, UO2_mat2, UO2_mat3)))



