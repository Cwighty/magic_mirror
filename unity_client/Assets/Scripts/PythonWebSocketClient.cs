using NativeWebSocket;
using UnityEngine;
using System;
using System.Collections.Generic;
using UnityEngine.SceneManagement;

public class WebSocketUnityClient : MonoBehaviour
{
    WebSocket websocket;
    private AudioPlayer audioPlayer;

    // Start is called before the first frame update
    async void Start()
    {
        DontDestroyOnLoad(gameObject);

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
                    break;
                case "transcribing":
                    SceneManager.LoadScene("Appear");
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
            HandleAudio(message.data);
        }
        else
        {
            Debug.LogWarning("Unknown message type!");
        }

    }

    void HandleAudio(string audioData)
    {
        GameObject audioPlayerObject = GameObject.Find("LipSyncContext");  // Replace with the actual name of the GameObject
        if (audioPlayerObject != null)
        {
            audioPlayer = audioPlayerObject.GetComponent<AudioPlayer>();
            audioPlayer.PlayAudioFromBase64(audioData);
        }
        else
        {
            Debug.LogError("AudioPlayer GameObject not found.");
        }
       
        async void OnApplicationQuit()
        {
            await websocket.Close();
        }
    }
}

[Serializable]
public class StatusMessage
{
    public string type;
    public string data;
}
