using System;
using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

public class AudioPlayer : MonoBehaviour
{
    public AudioSource audioSource;

    private void Start()
    {
        audioSource = GetComponent<AudioSource>();
    }

    public void PlayAudioFromBase64(string base64EncodedString)
    {
        byte[] mp3Bytes = System.Convert.FromBase64String(base64EncodedString);
        string tempFile = Path.Combine(Application.temporaryCachePath, "temp.mp3");
        File.WriteAllBytes(tempFile, mp3Bytes);
        StartCoroutine(PlayMP3(tempFile));
    }

    private IEnumerator PlayMP3(string filePath)
    {
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip("file://" + filePath, AudioType.MPEG))
        {
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = DownloadHandlerAudioClip.GetContent(www);
                audioSource.clip = clip;
                audioSource.Play();
            }
            else
            {
                Debug.LogError("Failed to load MP3: " + www.error);
            }
        }
        File.Delete(filePath);  // Optionally, delete the temp file after loading
    }

}

