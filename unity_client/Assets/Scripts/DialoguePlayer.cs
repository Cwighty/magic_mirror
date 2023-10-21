using System.Collections;
using UnityEngine;
using System.IO;

public class AudioPlayer : MonoBehaviour
{
    public string folderPath = "Your/Folder/Path/Here"; // Replace with your folder path
    public AudioSource audioSource;

    private void Start()
    {
        audioSource = GetComponent<AudioSource>(); // Get the AudioSource component
        StartCoroutine(PlayAndDeleteAudio());
    }

    private IEnumerator PlayAndDeleteAudio()
    {
        string[] files = Directory.GetFiles(folderPath, "*.mp3");

        if (files.Length > 0)
        {
            string filePath = files[0]; // Take the first file found

            // Load audio clip from the file path
            WWW www = new WWW("file://" + filePath);
            yield return www;
            AudioClip clip = www.GetAudioClip();

            if (clip != null)
            {
                audioSource.clip = clip;
                audioSource.Play();

                // Wait until the audio has finished playing
                yield return new WaitForSeconds(clip.length);

                // Delete the file
                File.Delete(filePath);
            }
            else
            {
                Debug.LogError("Could not load audio clip.");
            }
        }
        else
        {
            Debug.LogWarning("No audio files found in the folder.");
        }
    }
}
