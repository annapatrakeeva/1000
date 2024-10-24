import openmc
import openmc.deplete

import openmc.model
from openmc import stats
from math import sqrt
import neutronics_material_maker as nmm
from mat import water_mat,  AbstractUO2, Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat,  B4C_mat, basket_mat, water_mat1, be_mat, Dy2O3TiO2_mat

openmc.config['cross_sections']='/home/ann/PycharmProjects/endfb-vii.1-hdf5/cross_sections.xml'


import matplotlib.pyplot as plt
from core import get_TVS_universe, basket_universe
from params import GeometryParams


import numpy as np
if __name__ == "__main__":
    top_surf=openmc.ZPlane(z0=177.5)
    bottom_surf=openmc.ZPlane(z0=-177.5)
    top_surf.boundary_type='reflective'
    bottom_surf.boundary_type='reflective'


    mats=[]
    mats_id=[]
    TVS_30AV5, mats_30AV5=get_TVS_universe(3.0, 2.4, False, 1, 0,False, 0, 0)
    mats += mats_30AV5
    mats_id = [mat.id for mat in mats]
    TVS_13AU, mats_13AU =get_TVS_universe(1.3, 0, False, 0, False, False,  0, 0)
    for mat in mats_13AU:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)

    TVS_22AU, mats_22AU=get_TVS_universe(2.2, 0, False, 0, False, False, False, 0)
    for mat in mats_22AU:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_22AU_10, mats_22AU_10 = get_TVS_universe(2.2, 0, 1, 0, False, False, False, 0)
    for mat in mats_22AU_10:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_39AWU, mats_39AWU=get_TVS_universe(4.0, 3.3, False, 1, 0, 1, 3.6, 0)
    for mat in mats_39AWU:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_390GO, mats_390GO=get_TVS_universe(4.0, 3.3, False, 1, 1, 1, 3.6, 0)
    for mat in mats_390GO:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_398GO, mats_398GO=get_TVS_universe(4.4, 3.3, False, 1, 1, 0, False, 0)
    for mat in mats_398GO:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_430GO, mats_430GO=get_TVS_universe(4.4, 3.6, False, 1, 1, 1, 4.0, 0)
    for mat in mats_430GO:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    TVS_439GO, mats_439GO=get_TVS_universe(4.4, 3.6, False, 1, 0, 0, False, 0)
    for mat in mats_439GO:
        if mat.id not in mats_id:
            mats.append(mat)
            mats_id.append(mat.id)
    materials = openmc.Materials([ Gd2O3_mat, helium_mat, E110_mat, E635_mat, steel_mat,  B4C_mat, basket_mat, water_mat, be_mat, Dy2O3TiO2_mat]+mats)
    all_water2_cell = openmc.Cell(fill=basket_mat)
    water2_universe = openmc.Universe(cells=(all_water2_cell, ))
    core_lat = openmc.HexLattice()
    core_lat.center = (0.0, 0.0)
    core_lat.pitch = [11*1.275*sqrt(3)]
    core_lat.outer = water2_universe
    core_lat.orientation = 'x'
    ring_1=[basket_universe]+[TVS_390GO]+[TVS_39AWU]*4+ [TVS_390GO] #42
    ring_1*=6
    ring_2=[TVS_30AV5] + [TVS_22AU] #36
    ring_2*=18
    ring_3=[TVS_22AU]+[TVS_13AU]*4 #30
    ring_3*=6
    ring_4=[TVS_13AU] + [TVS_30AV5] + [TVS_22AU_10] +[TVS_30AV5] #24
    ring_4*=6
    ring_5= [TVS_22AU] + [TVS_13AU]+[TVS_13AU] #18
    ring_5*=6
    ring_6= [TVS_30AV5] + [TVS_22AU] #12
    ring_6*=6
    ring_7=[TVS_13AU]*6
    ring_8=[TVS_30AV5]
    core_lat.universes = [ring_1,  ring_2, ring_3, ring_4, ring_5, ring_6, ring_7, ring_8]

    outer2_surf = openmc.ZCylinder(r=173.5, boundary_type='vacuum')

    core_cell = openmc.Cell(fill=core_lat, region=-outer2_surf  & -top_surf & +bottom_surf )
    coolant=openmc.ZCylinder(r=174.5)
    barrel=openmc.ZCylinder(r=181)
    coolant2=openmc.ZCylinder(r=206.8)
    rpv=openmc.ZCylinder(r=226.75, boundary_type='vacuum')
    coolant_cell=openmc.Cell(fill=water_mat, region=-coolant & +outer2_surf  & -top_surf & +bottom_surf )
    barrel_cell=openmc.Cell(fill=steel_mat, region=-barrel & +coolant  & -top_surf & +bottom_surf )
    coolant2_cell=openmc.Cell(fill=water_mat, region=-coolant2 & + barrel  & -top_surf & +bottom_surf )
    rpv_cell=openmc.Cell(fill=steel_mat, region=-rpv & +coolant2 & -top_surf & +bottom_surf )
    materials.export_to_xml()
    params = GeometryParams()
    geometry=openmc.Geometry()
    geometry.root_universe=openmc.Universe( universe_id=0, cells=[core_cell, coolant_cell, barrel_cell, coolant2_cell, rpv_cell])
    settings=openmc.Settings()
    settings.temperature={'method': 'interpolation'}
    uniform_dist = stats.Box([-90, -90, -355 / 2], [90, 90, 355 / 2], only_fissionable=True)
    source = openmc.source.Source(space=uniform_dist)
    source.time = stats.Uniform(0, 1)
    settings.source = source
    tallies_file = openmc.Tallies()
    fiss_rate = openmc.Tally(name='fiss. rate')
    abs_rate = openmc.Tally(name='abs. rate')
    n_rate = openmc.Tally(name='n_rate')

    fiss_rate.scores = ['nu-fission']
    abs_rate.scores = ['absorption']
    n_rate.scores = ['(n,2n)']
    tallies_file += (fiss_rate, abs_rate, n_rate)
    tallies_file.export_to_xml()
    settings.batches = 1000
    settings.particles = 80000
    settings.inactive = 100
    #settings.trace=(1, 1, 25722)
    #settings.max_tracks = 1000
    #settings.tracks=[
    #    (1, 1, 28479),
    #    (1, 1, 24983)
    #]
    #trace2=settings.trace=(1, 1, 24983)
    #trace3=settings.trace=(1, 1, 20593)
    #settings_file+=(trace1, trace2, trace3)
    #trace_file.export_to_xml()
    settings.max_lost_particles=2000
    #settings.max_write_lost_particles
    #power = (3000.0e6)/163  # watts
    model = openmc.Model(geometry, materials, settings)
    #chain_file = '/home/ann/PycharmProjects/1000/library/chain_endfb71_pwr.xml'
    #operator = openmc.deplete.CoupledOperator(model, chain_file)
    #timesteps = [ (2,'MWd/kg'), (4,'MWd/kg'), (6,'MWd/kg'), (8,'MWd/kg'), (10,'MWd/kg'), (12,'MWd/kg'), (14,'MWd/kg'), (15,'MWd/kg'), (20,'MWd/kg'), (40, 'MWd/kg')]  # days
    #integrator=openmc.deplete.PredictorIntegrator(operator, timesteps,  power_density=108.0e6, timestep_units='MWd/kg')


    #openmc.deplete.CECMIntegrator(op, timesteps, power, timestep_units='d').integrate()
    #results = openmc.deplete.Results("depletion_results.h5")
    #time, keff = results.get_keff()

    #settings.run_mode = 'fixed source'
    #cecm = openmc.deplete.CECMIntegrator(operator, dt, power)
    #cecm.integrate()
    #source.strength = 18e0




    colors = {water_mat: (32, 178, 170), water_mat1: (124, 252, 0), B4C_mat: (255, 255, 255)}
    color_data = dict(color_by='material', colors=colors)
    width = np.array([20 *16, 50 * 16, ])
    scale = 1
    fig, ax = plt.subplots(2, 2)

    geometry.root_universe.plot(width=width / scale, pixels=(100, 100), basis='xz', **color_data,
                  origin=(0, 0, GeometryParams.tvel_heigh / 2 - 1), axes=ax[0][0])
    geometry.root_universe.plot(width=width / scale, pixels=(100, 100), basis='xz', **color_data, origin=(0, 0, 0), axes=ax[1][1])
    geometry.root_universe.plot(width=width / scale, pixels=(100, 100), basis='xz', **color_data,
                  origin=(0, 0, -GeometryParams.tvel_heigh / 2 + 1),
                  axes=ax[0][1])
    geometry.root_universe.plot(width=width / scale, pixels=(10000, 10000), basis='xy', **color_data, origin=(0, 0, 0), axes=ax[1][0])

    # ...and by openmc.Plots
    plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
    for i in range(4):
        plots[i].width = width
        plots[i].pixels = (5000, 5000)
        plots[i].basis = 'xz'
        plots[i].color_by = 'material'
        plots[i].colors = colors
    plots[0].origin = (0, 0, GeometryParams.tvel_heigh / 2 - 1)
    plots[2].origin = (0, 0, -GeometryParams.tvel_heigh / 2 - 1)
    plots[-1].basis = 'xy'

    plots = openmc.Plots(plots)



    #track=openmc.Track[('particle_2_50937.h5')]
    #print(track)
    plots.export_to_xml()
    settings.export_to_xml()
    geometry.export_to_xml()
    #model.export_to_xml('model.xml')
    openmc.plot_geometry()
    openmc.run()