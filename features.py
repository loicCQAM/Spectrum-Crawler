import librosa
import json
import requests
import os


def librosa_extract(song_url):
    # https://librosa.github.io/librosa/feature.html

    features = {}
    path = download_from_url(song_url)
    try :

        y , sr = librosa.load(path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr) # Compute a chromagram from a waveform or power spectrogram.
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr) # Constant-Q chromagram
        chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr) # Computes the chroma variant "Chroma Energy Normalized" (CENS)
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr) # Compute a mel-scaled spectrogram
        melspectrogram = librosa.feature.melspectrogram(y=y, sr=sr) # Compute a mel-scaled spectrogram
        mfcc = librosa.feature.mfcc(y=y, sr=sr) # Mel-frequency cepstral coefficients (MFCCs)
        rms = librosa.feature.rms(y=y) # Compute root-mean-square (RMS) value for each frame, either from the audio samples y or from a spectrogram S
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr) # Compute the spectral centroid
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr) # Compute p th-order spectral bandwidth
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr) # Compute spectral contrast
        spectral_flatness = librosa.feature.spectral_flatness(y=y) # Compute spectral flatness
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr) # Compute roll-off frequency
        poly_features = librosa.feature.poly_features(y=y, sr=sr) # Get coefficients of fitting an nth-order polynomial to the columns of a spectrogram
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr) # Computes the tonal centroid features (tonnetz)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y) # Compute the zero-crossing rate of an audio time series

        features['estimated_tempo'] = tempo
        features['beat_times'] = json.dumps(beat_times.tolist())
        features['chroma_stft'] = json.dumps(chroma_stft.tolist())
        features['chroma_cqt'] = json.dumps(chroma_cqt.tolist())
        features['chroma_cens'] = json.dumps(chroma_cens.tolist())
        features['melspectrogram'] = json.dumps(melspectrogram.tolist())
        features['mfcc'] = json.dumps(mfcc.tolist())
        features['rms'] = json.dumps(rms.tolist())
        features['spectral_centroid'] = json.dumps(spectral_centroid.tolist())
        features['spectral_bandwidth'] = json.dumps(spectral_bandwidth.tolist())
        features['spectral_contrast'] = json.dumps(spectral_contrast.tolist())
        features['spectral_flatness'] = json.dumps(spectral_flatness.tolist())
        features['spectral_rolloff'] = json.dumps(spectral_rolloff.tolist())
        features['poly_features'] = json.dumps(poly_features.tolist())
        features['tonnetz'] = json.dumps(tonnetz.tolist())
        features['zero_crossing_rate'] = json.dumps(zero_crossing_rate.tolist())

    except Exception as e:
        features = {}
        print("Could not import features from librosa : " + str(e))
    finally:
      delete_file(path)
      return features

def download_from_url(url):
    local_filename = url.split('/')[-1] + '.mp3'
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
    # CONVERT SONG TO WAV!!
    return local_filename

def delete_file(file_path):
    try:
        os.remove(file_path)
    except :
        print("Warning, could not delete audio file '" + file_path + "' after use.")

# # Create spectrogram graph
# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 4))
# librosa.display.specshow(librosa.power_to_db(melspectrogram, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Mel spectrogram')
# plt.tight_layout()
# plt.show()