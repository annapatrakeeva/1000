import openmc
from mat import  water_mat,  AbstractUO2, Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat, Dy2O3TiO2_mat, B4C_mat, basket_mat, water_mat1
from math import sqrt
from config import *
import random
top_surf=openmc.ZPlane(z0=177.5)
bottom_surf=openmc.ZPlane(z0=-177.5)
top_surf.boundary_type = 'reflective'
bottom_surf.boundary_type = 'reflective'
water_b_surf = openmc.model.HexagonalPrism(edge_length=23.6 / sqrt(3), orientation='y', boundary_type='transmission')
basket_cell = openmc.Cell(fill=basket_mat, region=-water_b_surf & +bottom_surf & -top_surf)
basket_universe = openmc.Universe(cells=[basket_cell])

def get_TVS_universe(enr, enr_tvegs, rods_inserted=False, tvegs=False, tvegs_5inner_ring=False,  outer_ring=False, outer_ring_enr=False, verbose=True):

     #if outer_ring and not outer_ring_enr:
         #raise Exception('Outer ring enrichment must be set')



    UO2_mat1 = AbstractUO2(enr).mat
    UO2_mat2=AbstractUO2(enr_tvegs).mat

    if tvegs:
        UO2_mat2 = openmc.Material.mix_materials(
   materials=[
        UO2_mat2,
        Gd2O3_mat,
    ],
    fracs=[0.95, 0.05],
    percent_type='vo')

    else:
        UO2_mat2 = UO2_mat1
    if outer_ring:
        UO2_mat3 = AbstractUO2(outer_ring_enr).mat
    else:
        UO2_mat3=UO2_mat1

    tvel_helium_surf=openmc.ZCylinder(r=r1_tvel)
    tvel_fuel_surf=openmc.ZCylinder(r=r2_tvel)
    tvel_helium2_surf=openmc.ZCylinder(r=r3_tvel)
    tvel_cladding_surf=openmc.ZCylinder(r=r4_tvel)

    central_surf1=openmc.ZCylinder(r=r1_central)
    central_surf2=openmc.ZCylinder(r=r2_central)

    cyz_absorber_surf=openmc.ZCylinder(r=r1_guide)
    cyz_steel_surf=openmc.ZCylinder(r=r2_guide)
    cyz_coolant_surf=openmc.ZCylinder(r=r3_guide)
    cyz_cladding_surf=openmc.ZCylinder(r=r4_guide)

    tvel_helium_lower_surf=openmc.ZCylinder(r=r1_tvel_low)
    tvel_cladding_lower_surf=openmc.ZCylinder(r=r2_tvel_low)

    tvel_helium_upper_surf=openmc.ZCylinder(r=r1_tvel_upper)
    tvel_cladding_upper_surf=openmc.ZCylinder(r=r2_tvel_upper)

    water_surf=openmc.model.HexagonalPrism(edge_length=1.275/sqrt(3), orientation='x', boundary_type='transmission')



    tvel1_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +bottom_surf & -top_surf)
    tvel1_fuel_cell=openmc.Cell(fill=UO2_mat1, region=+tvel_helium_surf & -tvel_fuel_surf & +bottom_surf & -top_surf)
    tvel1_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf  & +bottom_surf & -top_surf)
    tvel1_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +bottom_surf & -top_surf)
    tvel1_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf & -water_surf & +bottom_surf & -top_surf)

    tvel2_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +bottom_surf & -top_surf)
    tvel2_fuel_cell=openmc.Cell(fill=UO2_mat2, region=+tvel_helium_surf & -tvel_fuel_surf & +bottom_surf & -top_surf)
    tvel2_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf  & +bottom_surf & -top_surf)
    tvel2_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +bottom_surf & -top_surf)
    tvel2_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf & -water_surf & +bottom_surf & -top_surf)

    tvel3_helium1_cell=openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +bottom_surf & -top_surf)
    tvel3_fuel_cell=openmc.Cell(fill=UO2_mat3, region=+tvel_helium_surf & -tvel_fuel_surf & +bottom_surf & -top_surf)
    tvel3_helium2_cell=openmc.Cell(fill=helium_mat, region=+tvel_fuel_surf & -tvel_helium2_surf  & +bottom_surf & -top_surf)
    tvel3_cladding_cell=openmc.Cell(fill=E110_mat, region=+tvel_helium2_surf & -tvel_cladding_surf & +bottom_surf & -top_surf)
    tvel3_water_cell=openmc.Cell(fill=water_mat, region=+tvel_cladding_surf & -water_surf & +bottom_surf & -top_surf)

    #tvel4_helium1_cell = openmc.Cell(fill=helium_mat, region=-tvel_helium_surf & +bottom_surf & -top_surf)
   # tvel4_fuel_cell = openmc.Cell(fill=UO2_mat4, region=+tvel_helium_surf & -tvel_fuel_surf & +bottom_surf & -top_surf)
    #tvel4_helium2_cell = openmc.Cell(fill=helium_mat,
           #                           region=+tvel_fuel_surf & -tvel_helium2_surf & +bottom_surf & -top_surf)
   # tvel4_cladding_cell = openmc.Cell(fill=E110_mat,
               #                        region=+tvel_helium2_surf & -tvel_cladding_surf & +bottom_surf & -top_surf)
   # tvel4_water_cell = openmc.Cell(fill=water_mat, region=+tvel_cladding_surf & water_surf & +bottom_surf & -top_surf)

    tvel1_universe=openmc.Universe(cells=[tvel1_helium1_cell, tvel1_fuel_cell, tvel1_helium2_cell, tvel1_cladding_cell, tvel1_water_cell])
    tvel2_universe=openmc.Universe(cells=[tvel2_helium1_cell, tvel2_fuel_cell, tvel2_helium2_cell, tvel2_cladding_cell, tvel2_water_cell])
    tvel3_universe=openmc.Universe(cells=[tvel3_helium1_cell, tvel3_fuel_cell, tvel3_helium2_cell, tvel3_cladding_cell, tvel3_water_cell])
    #tvel4_universe = openmc.Universe(cells=[tvel4_helium1_cell, tvel4_fuel_cell, tvel4_helium2_cell, tvel4_cladding_cell, tvel4_water_cell])


    if rods_inserted:
        guide_mat = B4C_mat
    else:
        guide_mat = water_mat

    guide_absorber_cell=openmc.Cell(fill=guide_mat, region=-cyz_absorber_surf & +bottom_surf & -top_surf)
    guide_steel_cell=openmc.Cell(fill=steel_mat, region=-cyz_steel_surf & +cyz_absorber_surf & +bottom_surf & -top_surf)
    guide_water1_cell=openmc.Cell(fill=water_mat, region=-cyz_coolant_surf & +cyz_steel_surf & +bottom_surf & -top_surf)
    guide_cladding_cell=openmc.Cell(fill=E635_mat, region=-cyz_cladding_surf & +cyz_coolant_surf & +bottom_surf & -top_surf )
    guide_water2_cell=openmc.Cell(fill=water_mat, region=+cyz_cladding_surf & -water_surf & +bottom_surf & -top_surf)

    guide_universe=openmc.Universe(cells=[guide_absorber_cell, guide_steel_cell, guide_water1_cell, guide_water1_cell, guide_cladding_cell, guide_water2_cell] )
    print('ghghhgg', guide_mat )
    central_cell1=openmc.Cell(fill=water_mat, region=-central_surf1 & +bottom_surf & -top_surf)
    central_cell2=openmc.Cell(fill=E635_mat, region=+central_surf1 & -central_surf2 & +bottom_surf & -top_surf)
    central_water_cell=openmc.Cell(fill=water_mat, region= +central_surf2 & -water_surf & +bottom_surf & -top_surf)

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
    fife_ring = [tvel1_universe] * 3 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [
    tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [
                  guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 2  # 36
    six_ring = [guide_universe] + [tvel1_universe] * 4  # 30
    six_ring *= 6
    if tvegs_5inner_ring:
     seven_ring = [tvel1_universe] * 3 + [tvel2_universe]
     seven_ring *= 6
    else:
     seven_ring = [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 4
     seven_ring *= 3
    eight_ring = [tvel1_universe] + [guide_universe] + [tvel1_universe]  # 18
    eight_ring *= 6
    nint_ring = [tvel1_universe] * 12  # 12
    ten_ring = [tvel1_universe] * 6
    inner_ring = [central_universe]
    lat.universes = [firts_ring, second_ring, third_ring, four_ring, fife_ring, six_ring, seven_ring, eight_ring, nint_ring, ten_ring, inner_ring]
    outer_surf=openmc.model.HexagonalPrism(edge_length=11*lat.pitch[0], orientation='y', boundary_type='reflective')
    TVS_cell = openmc.Cell(fill=lat, region=-outer_surf & +bottom_surf & -top_surf)
    TVS_universe=openmc.Universe(cells=[TVS_cell])
    if verbose:
        print(lat)
    return TVS_universe, list(set((UO2_mat1, UO2_mat2, UO2_mat3))) + [guide_mat]

