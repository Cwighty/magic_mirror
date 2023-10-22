using NativeWebSocket;
using UnityEngine;
using System;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using System.Diagnostics;
using Debug = UnityEngine.Debug;
using System.Collections;

public class WebSocketUnityClient : MonoBehaviour
{
    WebSocket websocket;
    private AudioPlayer audioPlayer;

    public AudioClip windClip;
    public AudioSource windAudioSource;

    public ParticleSystem fireParticles;
    public AudioSource fireAudioSource;
    public AudioClip fireClip;

    public float windFadeOutDuration = 2.0f;  // Duration in seconds for the audio to fade out
    private bool windIsFadingOut = false;

    // Start is called before the first frame update
    async void Start()
    {
        DontDestroyOnLoad(gameObject);
        SceneManager.sceneLoaded += OnSceneLoaded;

        websocket = new WebSocket("ws://localhost:8765");
        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Connection closed!");
        };

        websocket.OnMessage += (bytes) =>
        {
            // Try to convert message bytes to UTF-8 string
            try
            {
                var message = System.Text.Encoding.UTF8.GetString(bytes);
                var status = JsonUtility.FromJson<StatusMessage>(message);

                HandleMessage(status);
            }
            catch (Exception e)
            {
                Debug.Log("Invalid message received! " + e.Message);
            }
        };

        // waiting for messages
        await websocket.Connect();
    }

    private void OnSceneLoaded(Scene arg0, LoadSceneMode arg1)
    {
        if (windAudioSource.isPlaying && !windIsFadingOut)
        {
            StartCoroutine(FadeOutAudio());
        }
    }

    void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        websocket.DispatchMessageQueue();
#endif
    }

    void HandleMessage(StatusMessage message)
    {
        if (message.type == "message")
        {
            switch (message.data)
            {
                case "listening":
                    Debug.Log("Listening...");
                    HandleListening();
                    break;
                case "transcribing":
                    HandleTranscribing();
                    break;
                case "processing":
                    Debug.Log("Processing...");
                    break;
                default:
                    Debug.LogWarning("Unknown message");
                    break;
            }
        }
        else if (message.type == "audio")
        {
            StartCoroutine(WaitAndPlayTtsResponse(message.data));
        }
        else
        {
            Debug.LogWarning("Unknown message type!");
        }

    }

    IEnumerator WaitAndPlayTtsResponse(string audioData)
    {
        yield return new WaitForSeconds(3);  // Wait for 1 second

        GameObject audioPlayerObject = GameObject.Find("LipSyncContext");
        if (audioPlayerObject != null)
        {
            audioPlayer = audioPlayerObject.GetComponent<AudioPlayer>();
            audioPlayer.PlayAudioFromBase64(audioData);
        }
        else
        {
            Debug.LogError("AudioPlayer GameObject not found.");
        }
    }

    void HandleListening()
    {
        if (SceneManager.GetActiveScene().name == "Nothing")
        {
            // Play the audio clip
            if (!windAudioSource.isPlaying) // Check to ensure it doesn't restart if already playing
            {
                windAudioSource.clip = windClip;
                windAudioSource.Play();
                DontDestroyOnLoad(windAudioSource);
            }
        }
    }
    
    void HandleTranscribing()
    {
        if (SceneManager.GetActiveScene().name == "Nothing")
        {
            if (!fireAudioSource.isPlaying)            {
                fireAudioSource.clip = fireClip;
                fireAudioSource.Play();
                DontDestroyOnLoad(fireAudioSource);
            }
            if (!fireParticles.isPlaying)
            {
                fireParticles.Play();
            }

            StartCoroutine(WaitAndChangeScene());
        }
        else
        {
            GameObject audioPlayerObject = GameObject.Find("LipSyncContext");
            if (audioPlayerObject != null)
            {
                audioPlayer = audioPlayerObject.GetComponent<AudioPlayer>();
                audioPlayer.PlayRandomQuickResponse();
            }
        }
    }
    IEnumerator WaitAndChangeScene()
    {
        yield return new WaitForSeconds(3);  // Wait for 3 seconds

        SceneManager.LoadScene("Appear");
    }

    IEnumerator FadeOutAudio()
    {
        windIsFadingOut = true;
        float startVolume = windAudioSource.volume;

        while (windAudioSource.volume > 0)
        {
            windAudioSource.volume -= startVolume * Time.deltaTime / windFadeOutDuration;
            yield return null;
        }

        windAudioSource.Stop();
        windAudioSource.volume = startVolume;

        Destroy(windAudioSource);
    }
}

[Serializable]
public class StatusMessage
{
    public string type;
    public string data;
}
