import librosa
import json


def librosa_extract(song_link):
    # https://librosa.github.io/librosa/feature.html

    features = {}
    
    try :

        # CONVERT SONG_LINK TO WAV!

        y , sr = librosa.load(song_link)

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

        # Compute the Fourier tempogram: the short-time Fourier transform of the onset strength envelope
        hop_length = 512
        oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
        tempogram = librosa.feature.fourier_tempogram(onset_envelope=oenv, sr=sr, hop_length=hop_length)

        feature['estimated_tempo'] = tempo
        feature['beat_times'] = json.dumps(beat_times)
        feature['chroma_stft'] = json.dumps(chroma_stft)
        feature['chroma_cqt'] = json.dumps(chroma_cqt)
        feature['chroma_cens'] = json.dumps(chroma_cens)
        feature['melspectrogram'] = json.dumps(melspectrogram)
        feature['mfcc'] = json.dumps(mfcc)
        feature['rms'] = json.dumps(rms)
        feature['spectral_centroid'] = json.dumps(spectral_centroid)
        feature['spectral_bandwidth'] = json.dumps(spectral_bandwidth)
        feature['spectral_contrast'] = json.dumps(spectral_contrast)
        feature['spectral_flatness'] = json.dumps(spectral_flatness)
        feature['spectral_rolloff'] = json.dumps(spectral_rolloff)
        feature['poly_features'] = json.dumps(poly_features)
        feature['tonnetz'] = json.dumps(tonnetz)
        feature['zero_crossing_rate'] = json.dumps(zero_crossing_rate)
        feature['tempogram'] = json.dumps(tempogram)

        return features

    except:
        print("Could not import features from librosa.")
        return []

# # Create spectrogram graph
# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 4))
# librosa.display.specshow(librosa.power_to_db(melspectrogram, ref=np.max), y_axis='mel', fmax=8000, x_axis='time')
# plt.colorbar(format='%+2.0f dB')
# plt.title('Mel spectrogram')
# plt.tight_layout()
# plt.show()