
library(shiny)
library(yaml)

# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Classifer"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         actionButton("bath","Bath",width="100%"),
         hr(),
         actionButton("kitchen", "Kitchen",width="100%"),
         hr(),
         actionButton("living", "Livingroom",width="100%"),
         hr(),
         actionButton("bedroom", "Bedroom",width="100%"),
         hr(),
         actionButton("empty", "empty_room",width="100%"),
         hr(),
         actionButton("corridor", "corridor",width="100%"),
         hr(),
         actionButton("house", "house",width="100%"),
         hr(),
         actionButton("floor_plan", "floor_plan",width="100%"),
         hr(),
         actionButton("balcony", "balcony",width="100%"),
         hr(),
         actionButton("other", "other",width="100%")
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
        imageOutput("myImage")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  config = read_yaml(file = "../shiny_config.yaml")

  mainPath = config$mainPath
  exportPath = config$exportPath
  imageType = config$imageType
  
  print(mainPath)
  listOfFiles = list.files(path = mainPath , pattern = paste0(".", imageType))
  print(listOfFiles)
  counter <- reactiveVal(1) 
  
  #Function to copy file to a category folder and then delete the original file
  moveFile <- function(path,exportPath,file,cate){
    file.copy(from=paste0(path, file), to=paste0(exportPath,cate))
    file.remove(paste0(path, file))
  }
  
  
  observeEvent(input$bath,{
    print("bathroom")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "bath_room")
    counter(counter()+1)
  })
  
  observeEvent(input$kitchen,{
    print("kitchen")
    moveFile(mainPath,exportPath, listOfFiles[counter()], "kitchen")
    counter(counter()+1)
  })
  
  observeEvent(input$bedroom,{
    print("sleeping_room")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "sleeping_room")
    counter(counter()+1)
  })
  
  observeEvent(input$living,{
    print("living_room")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "living_room")
    counter(counter()+1)
  })
  
  
  
  observeEvent(input$empty,{
    print("empty_room")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "empty_room")
    counter(counter()+1)
  })
  
  
  observeEvent(input$corridor,{
    print("corridor")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "corridor")
    counter(counter()+1)
  })  
  
  
  observeEvent(input$house,{
    print("house")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "house")
    counter(counter()+1)
  })  
  
  observeEvent(input$floor_plan,{
    print("floor_plan")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "floor_plan")
    counter(counter()+1)
  })  
  
  observeEvent(input$balcony,{
    print("balcony")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "balcony")
    counter(counter()+1)
  })  
  
  observeEvent(input$other,{
    print("other")
    moveFile(mainPath, exportPath, listOfFiles[counter()], "other")
    counter(counter()+1)
  })  
  
  output$myImage <- renderImage({
    # When input$n is 3, filename is ./images/image3.jpeg
    
    if(counter() < length(listOfFiles)){
      filename <- normalizePath(file.path(paste0(mainPath, listOfFiles[counter()])))
    }else{
      filename <- normalizePath(file.path(paste0(mainPath, listOfFiles[counter()])))
    }
    
    # Return a list containing the filename and alt text
    return(list(src = filename,alt = paste("Image")))
    
  }, deleteFile = FALSE)
  
}

# Run the application 
shinyApp(ui = ui, server = server)

