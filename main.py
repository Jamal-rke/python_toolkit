

# main.py

from dataset_generator import generate_dataset

source_folder = r"D:\Python\Python_gen_toolkit\ref\P501_C_english_f1_FB_48k.wav"
output_folder = r"D:\Python\Python_gen_toolkit\deg"
noise_folder = r"D:\Python\Python_gen_toolkit\deg\noise\Inside_Train_Noise2_binaural ( 0.00-30.00 s).wav"
num_files = 100



# Example condition table
condition_table =[
    {
        'filter': 'highpass',
        'bp_high': 8000,
        'arb_filter': 'x',
        'timeclipping': 'x',
        'tc_fer': 5,
        'tc_nburst': 1,
        'wbgn': 'x',
        'wbgn_snr': 10,
        'p50mnru': 'x',
        'p50_q': 0.2,
        'asl_in': 'x',
        'asl_in_level': -26,
        'asl_out': 'x',
        'asl_out_level': -26,
        'clipping': 'x',
        'cl_th': 0.5,
        'bgn': 'x',
        'bgn_file': 'background_noise.wav',
        'bgn_snr': 10,
        'codec1': 'amrnb',
        'bMode1': 'mode1',
        'plcMode1': 'random',
        'FER1': 5,
        'codec2': 'skip',
        'bMode2': '',
        'plcMode2': '',
        'FER2': '',
        'codec3': 'skip',
        'bMode3': '',
        'plcMode3': '',
        'FER3': '',
        'dist_post_codec': ''},
    ]
    # Add more conditions as needed


# for condition in condition_table:
#     print(condition,end="  ")


generate_dataset(source_folder, noise_folder, output_folder, num_files)
