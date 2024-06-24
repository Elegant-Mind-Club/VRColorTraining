using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using TMPro;

public class AutoSelectInputField : MonoBehaviour
{
    public TMP_InputField nameInputField;

    void Start()
    {
        nameInputField = GameObject.Find("nameInputField").GetComponent<TMP_InputField>(); ; // UI object for name Input
        // Set the input field as the currently selected object
        EventSystem.current.SetSelectedGameObject(nameInputField.gameObject, null);

        // Optionally, focus on the input field to start typing immediately
        nameInputField.ActivateInputField();
    }
}
