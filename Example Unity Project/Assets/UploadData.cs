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
    public TMP_InputField nameField;
    public TMP_InputField idField;
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
        if (nameField.text == "" ||
            idField.text == "" ||
            scoreField.text == "" ||
            difficultyField.text == "" ||
            achievementsField.text == "")
        {
            responseText.text = "Fill in all fields!";
            return;
        }
        
        StartCoroutine(Upload());
    }
    
    IEnumerator Upload()
    {
        WWWForm form = new WWWForm();
        form.AddField("playerName", nameField.text);
        form.AddField("playerId", idField.text);
        form.AddField("score", scoreField.text);
        form.AddField("difficulty", difficultyField.text);
        form.AddField("achievements", achievementsField.text);
        
        UnityWebRequest www = UnityWebRequest.Post(url, form);
        www.SetRequestHeader("Authentication", "Bearer 1234");

        using (www)
        {
            yield return www.SendWebRequest();
            
            if (!string.IsNullOrWhiteSpace(www.error))
            {
                // Show the error message from the response
                responseText.text = www.downloadHandler.text;
            }
            else
            {
                responseText.text = "Upload complete!";
            }
        }
    }
}
