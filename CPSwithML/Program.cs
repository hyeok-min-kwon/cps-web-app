using CPSwithML.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();

// HttpClient 및 PredictionService 등록
builder.Services.AddHttpClient<PredictionService>(client =>
{
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Configuration 설정 (appsettings.json에서 API URL 읽기)
builder.Configuration.AddJsonFile("appsettings.json", optional: true, reloadOnChange: true);

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();
