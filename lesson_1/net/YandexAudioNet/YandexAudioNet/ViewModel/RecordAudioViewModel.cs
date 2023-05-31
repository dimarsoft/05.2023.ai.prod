using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
//using NAudio;
using NAudio.Wave;

namespace YandexAudioNet.ViewModel;
//https://qna.habr.com/q/405123

public class RecordAudioViewModel
{
    private readonly WaveInEvent _waveIn = new WaveInEvent();
    private readonly string _outputFilePath;
    private WaveFileWriter _waveFile;

    public RecordAudioViewModel()
    {
        var outputFolder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "NAudio");
        Directory.CreateDirectory(outputFolder);
        _outputFilePath = Path.Combine(outputFolder,"recorded.wav");        
    }
    public void StartRecord()
    {
        _waveFile = new WaveFileWriter(_outputFilePath, _waveIn.WaveFormat);
        _waveIn.DataAvailable += WaveInOnDataAvailable;
        _waveIn.StartRecording();
    }

    private void WaveInOnDataAvailable(object sender, WaveInEventArgs e)
    {
        _waveFile.Write(e.Buffer, 0, e.BytesRecorded);
        if (_waveFile.Position > _waveIn.WaveFormat.AverageBytesPerSecond * 30)
        {
            StopRecord();
        }        
    }

    public void StopRecord()
    {
        _waveIn.StopRecording();
        _waveIn.DataAvailable -= WaveInOnDataAvailable;
    }
    public async Task<string> Synthesize(string text)
    {
        //const string apyKey = "YCOO72iRl-05BettepCAZWptHq1iusTS9o4HvGn0"; // Укажите IAM-токен.
        const string apyKey = "AQVN2ZUi8hE02NqLZnOR4zioczP7YKDwGxJdjsyM";
        //const string folderId = "<идентификатор каталога>"; // Укажите идентификатор каталога.

        HttpClient client = new ();
        client.DefaultRequestHeaders.Add("Authorization", $"Api-Key {apyKey}");
        var values = new Dictionary<string, string>
        {
            { "text", text },
            { "lang", "ru-RU" },
            { "voice", "filipp" },
           // { "folderId", folderId }
        };
        var content = new FormUrlEncodedContent(values);
        var response = await client.PostAsync("https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize", content);
        if (response.StatusCode != HttpStatusCode.OK)
        {
            Console.Write(response);
            var responses = await response.Content.ReadAsStringAsync();
            return responses;
        }
        var responseBytes = await response.Content.ReadAsByteArrayAsync();
        var fileName = $"{_outputFilePath}.ogg";
        await File.WriteAllBytesAsync(fileName, responseBytes);

        return $"{fileName} is ready";
    }
}