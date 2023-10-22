using System;
using System.Collections;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

public class AudioPlayer : MonoBehaviour
{
    public AudioSource audioSource;
    public AudioClip[] quickResponses;

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

    public void PlayRandomQuickResponse()
    {
        if (quickResponses.Length == 0) return;  // Ensure there are audio clips to choose from

        int randomIndex = UnityEngine.Random.Range(0, quickResponses.Length);  // Get a random index
        audioSource.clip = quickResponses[randomIndex];  // Assign the random audio clip to the audio source
        audioSource.Play();  // Play the audio source
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

