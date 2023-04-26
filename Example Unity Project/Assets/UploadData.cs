using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using UnityEngine.UI;
using TMPro;

public class UploadData : MonoBehaviour
{
    // This is the URL where you will handle the form input.
    // You can use any URL you like, but make sure a compatible server is running.
    public string url = "http://127.0.0.1:5000/post";
    
    // Set the field variables we'll need to use later
    public TMP_InputField scoreField;
    public TMP_InputField difficultyField;
    public TMP_InputField achievementsField;
    // public Button UploadButton;
    
    // And get the panel with the text we want to change to show the server response
    public TextMeshProUGUI responseText;

    private void Start()
    {
        // Set the text to be blank to start
        responseText.text = "";
    }

    public void SubmitForm()
    {
        // Check that the important fields are filled in
        if (scoreField.text == "" || difficultyField.text == "")
        {
            responseText.text = "Score and Difficulty are required";
            return;
        }
        
        StartCoroutine(Upload());
    }
    
    IEnumerator Upload()
    {
        WWWForm form = new WWWForm();
        form.AddField("score", scoreField.text);
        form.AddField("difficulty", difficultyField.text);
        form.AddField("achievements", achievementsField.text);

        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            yield return www.SendWebRequest();
            
            if (!string.IsNullOrWhiteSpace(www.error))
            {
                responseText.text = "Error uploading: " + www.error;
            }
            else
            {
                responseText.text = "Upload complete!" + www.error;
            }
        }
    }
}
