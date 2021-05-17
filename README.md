# Stardreams

## Team

This is the final project of our fourth semester "Software Construction and Decision Making" course. The team members are: 
- Marcia Lechuga López
- Agustín Abreu Callejas
- Iñigo Enique Zepeda Ceballos
- Diego Enrique Jiménez Urgell

## Motivation

During this ten-week course, we worked with a non-profit organization called [Fundación Movimiento STEAM](https://movimientosteam.org), which leads a national effort to boost the STEM ecosystem in Mexico. One of the aspects they focus the most on is Education, since in Mexico not many children want to study something related with STEM. In order to motivate children and create educative programs tailored to their needs, it is necessary to have some statistical indicators that help with the decision making process. The challenge assigned to us was to create a system that generates these indicators. By using a videogame we would retrieve data from the players such as gender, age, preferred STEM branch, etc. This information would be stored in a database, and then some statistics and graphs would be displayed in a website. 
 
To solve this, we learned about videogames development with Unity and web development with Django in the backend and HTML, jQuery, and Bootstrap in the frontend. We built a user management system so that the player would sign up at our website, then login at the videogame and play. For our videogame we created four different miniworlds with a minigame, each one related to a specific STEM area. Some data from the game, such as time spent playing and the completed levels is sent to our database. Then, users can login at the website to see a personal dashboard with their statistics and information. Professor accounts can also be created, which allow to monitor the progress and interests of students by providing them a unique autogenerated token. The data generated by all the players is is used to create STEM indicators, which are displayed in a public dashboard.

In our videogame, each night a child goes to sleep and dreams with different worlds, where he has to help some creatures, the *Starfriends*, to solve different problems. In order to do so, the player first learns some basic concepts from each STEM area and then applies the acquired knwoledge to solve a minigame. As everything occures while the child is sleeping, we chose the name *Stardreams*. 

## How to use our system? 

### Creating an account

1. Visit our [website](http://52.171.199.75:8000/) and click on " Mi Cuenta" (My account) on the navbar. 
2. As you are a new user, click on "Registrate aquí" (Sign up). 
3. Select either Student or Professor in order to create your account
4. Fill in the form with the required information. 
  **Note:** If you are a student and your professor gave you her unique token, you should paste it in the form. Otherwise, this is optional. 
  
| Signup Form |
|---|
| [![Screen-Shot-2021-05-01-at-15-54-31.png](https://i.postimg.cc/Rh4shCnh/Screen-Shot-2021-05-01-at-15-54-31.png)](https://postimg.cc/sQH90rmC)  |

5. You will be redirected to your private dashboard, which will be empty at first. 
  **Note:** If you are a professor, your dashboard will display your unique token. You should give this to your students before they sign up. 
  
### Playing the videogame
6. Open the videogame, either by downloading an installer or by clicking on the "Juégalo online" (Play online) button. **Note:** The online version only works in Google Chrome or Microsoft Edge browsers. 
7. Ckick on "Jugar" and login with the username and password from the website. 
8. Explore the main labyrint and talk with the *Starfriends*

| Main Labyrint |
|---|
|[![Screen-Shot-2021-05-01-at-16-30-58.png](https://i.postimg.cc/br0QGQjf/Screen-Shot-2021-05-01-at-16-30-58.png)](https://postimg.cc/PvxL9vxS)|

9. Explore each miniworld and complete its minigame. There are five different miniworlds, one for each STEM branch. The following example shows the Technology miniworld and minigame. 

| Technology miniworld | 
|---|
| [![Screen-Shot-2021-05-01-at-17-45-09.png](https://i.postimg.cc/nhmnqTPm/Screen-Shot-2021-05-01-at-17-45-09.png)](https://postimg.cc/BjqW05sZ) | 


| Technology minigame |
|---|
 | [![Screen-Shot-2021-05-01-at-16-37-52.png](https://i.postimg.cc/L4jk0MgQ/Screen-Shot-2021-05-01-at-16-37-52.png)](https://postimg.cc/bdN2sWT1)  |

10. When you win a minigame, you will obtain a special artifact displayed in the inventory. 
11. To close the game, go to the main menu and click on "Salir". 

### Obtaining insights from the dashboards
12. When you login again to the website, you will see that your private dashboard has been updated and shows statistics and other personal information. If you are a professor, you will be able to track the progress of each of your students and their preferred STEM branch. 

| Student Dashboard  | 
|---|
| [![Screen-Shot-2021-05-01-at-14-41-10.png](https://i.postimg.cc/BvNG4zzx/Screen-Shot-2021-05-01-at-14-41-10.png)](https://postimg.cc/v11Kv0bB)  |


 | Professor Dashboard  |
 |---|
 | [![Screen-Shot-2021-05-01-at-16-25-23.png](https://i.postimg.cc/BbBzBPG2/Screen-Shot-2021-05-01-at-16-25-23.png)](https://postimg.cc/vxDXQBTm)  |
 
13. If you visit the "Indicadores" page, you can see several graphs and calculations that give a lot of insight into the interests and characteristics of the players and the teachers. In this way, we created STEM indicators while the children learnt something useful and had fun. 

| Sample indicators from the website |
|---|
| [![Screen-Shot-2021-05-01-at-17-49-18.png](https://i.postimg.cc/qqnd2vmT/Screen-Shot-2021-05-01-at-17-49-18.png)](https://postimg.cc/hQSwBcWy) |

**Enjoy Stardreams!**
