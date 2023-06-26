from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QScrollArea, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap



class ResourcesPage(QWidget):

    def __init__(self):
        super(ResourcesPage, self).__init__()
        
        # Declare layout
        outer_layout = QVBoxLayout()

        # Declare tabs
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        news = NewsTab()
        tools = ToolsTab()
        apps = OtherAppsTab()

        # Define tabs
        tab_views = {
            'New Outlets': news,
            'Tools': tools,
            'Other Apps': apps
        }

        for view_name, view in tab_views.items():
            tabs.addTab(view, view_name)

        # Add widgets to layout
        outer_layout.addWidget(tabs)

        # Set layout to main window
        self.setLayout(outer_layout)

class HyperlinkLabel(QLabel):
    def __int__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)

class RWidget(QFrame):
    def __init__(self, img, hyperlink, title, descript):
        super(RWidget, self).__init__()

        self.setFixedHeight(150)
        self.setFixedWidth(915)
        self.setStyleSheet("background-color: #454545")
        
        #Define layout
        outer_layout = QHBoxLayout()
        right_layout = QVBoxLayout()

        # Declare Image
        picture = QLabel()
        pixmap = QPixmap(img)
        pixmap_scaled = pixmap.scaledToHeight(100)
        picture.setPixmap(pixmap_scaled)

        # Declare Header/hyperlink
        linkTemplate = '<a href={0}>{1}</a>'
        
        header = HyperlinkLabel(self)
        header.setStyleSheet('font-size: 30px')
        header.setText(linkTemplate.format(hyperlink, title))
    
        # Declare Description
        description = QLabel(descript)
        description.setMaximumWidth(700)
        description.setWordWrap(True)

        # Add labels to right layout
        right_widget = QWidget()
        right_layout.addWidget(header)
        right_layout.addWidget(description)
        right_widget.setLayout(right_layout)

        # Add widgets and sublayouts to main layout
        outer_layout.addWidget(picture, alignment=Qt.AlignmentFlag.AlignLeading)
        outer_layout.addWidget(right_widget, 10)

        # end = QLabel()
        # outer_layout.addWidget(end, alignment=Qt.AlignmentFlag.AlignRight)
        # outer_layout.addStretch()

        # Set layout to main widget
        self.setLayout(outer_layout)
        
class NewsTab(QWidget):
    def __init__(self):
        super(NewsTab, self).__init__()

        # Define Layout
        outer_layout = QVBoxLayout()
        scroll = QScrollArea()        

        # Define news list
        news_list = QWidget()
        
        news_outlets = [
            RWidget('images/resources/hackerNews.png',
                'https://news.ycombinator.com',
                'Hacker News',
                "Hacker News is a social news website focusing on computer "
                "science and entrepreneurship. It is run by the investment "
                "fund and startup incubator Y Combinator."),
            RWidget('images/resources/danielMiessler.png',
                'https://danielmiessler.com',
                'Daniel Miessler',
                "Exploring the intersection of security, technology, "
                "and society—and what might be coming next."),
            RWidget('images/resources/itSecurityGuru.png',
                'https://www.itsecurityguru.org',
                'IT Security Guru',
                "IT Security Guru is the home of IT Security and "
                "Cybersecurity news in the UK, Europe and the World. "
                "Get the latest industry news and articles here."),
            RWidget('images/resources/cso.png',
                'https://www.csoonline.com',
                'CSO',
                "CSO serves enterprise security decision-makers and users "
                "with the critical information they need to stay ahead of "
                "evolving threats and defend against criminal cyberattacks."),
            RWidget('images/resources/welivesecurity.png',
                'https://www.welivesecurity.com',
                'We Live Security',
                "The latest news, research, cyber threats, malware "
                "discoveries, mobile security, ransomware, and insight from "
                "the ESET experts. WeLiveSecurity comes from the brains at "
                "ESET - experienced researchers with in-depth knowledge of "
                "the latest threats & security trends."),
            RWidget('images/resources/darkreading.png',
                'https://www.darkreading.com',
                'DARK Reading',
                "Cyber security's comprehensive news site is now an online "
                "community for security professionals, outlining cyber "
                "threats and the technologies for defending against them."),
            RWidget('images/resources/securityweekly.png',
                'https://www.securityweek.com',
                'Security Weekly',
                "Threatpost, is an independent news site which is a leading "
                "source of information about IT and business security for "
                "hundreds of thousands of professionals."),
            RWidget('images/resources/threatpost.png',
                'https://threatpost.com',
                'Threast Post',
                "IT Security News and Information Security News, Cyber "
                "Security, Network Security, Enterprise Security Threats, "
                "Cybercrime News and more. Information Security Industry "
                "Expert insights and analysis from IT security experts "
                "around the world.")
            ]

        # Declare list of News Outlets
        news_list_layout = QVBoxLayout()
        for news in news_outlets:
            news_list_layout.addWidget(news)

        news_list.setLayout(news_list_layout)
        scroll.setWidget(news_list)
        outer_layout.addWidget(scroll)
            
        # Set layout to main window
        self.setLayout(outer_layout)

class ToolsTab(QWidget):
    def __init__(self):
        super(ToolsTab, self).__init__()

        # Define Layout
        outer_layout = QVBoxLayout()
        scroll = QScrollArea()        

        # Define news list
        tools_list = QWidget()
        
        tools = [
            RWidget('images/resources/lookingGlass.png',
                'https://map.lookingglasscyber.com',
                'LookingGlass Threat Map',
                "LookingGlass delivers the most comprehensive threat "
                "intelligence-driven solutions in the market enabling "
                "security teams to efficiently and effectively address "
                "threats throughout the cyber threat lifecycle."),
            RWidget('images/resources/hibp.png',
                'https://haveibeenpwned.com/#:~:text=Breaches%20you%20were%20pwned%20in,your%20other%20services%20at%20risk.',
                'Have I Been Pwned',
                "HIBP enables you to discover if your account was exposed in "
                "most of the data breaches by directly searching the system. "
                "However, certain breaches are particularly sensitive in that "
                "someone's presence in the breach may adversely impact them "
                "if others are able to find that they were a member of the site."),
            RWidget('images/resources/passwordMonster.png',
                'https://www.passwordmonster.com',
                'Password Monster',
                "The password strength calculator uses a variety of "
                "techniques to check how strong a password is. It uses "
                "common password dictionaries, regular dictionaries, first "
                "name and last name dictionaries and others"),
            RWidget('images/resources/osintFramework.png',
                'https://osintframework.com',
                'OSINT Framework',
                "OSINT framework focused on gathering information from free "
                "tools or resources. The intention is to help people find "
                "free OSINT resources. Some of the sites included might "
                "require registration or offer more data for $$$, but you "
                "should be able to get at least a portion of the available "
                "information for no cost."),
            RWidget('images/resources/nist.png',
                'https://nvd.nist.gov',
                'National Vulnerability Database',
                "The NVD is the U.S. government repository of standards "
                "based vulnerability management data represented using the "
                "Security Content Automation Protocol (SCAP). The NVD "
                "includes databases of security checklist references, "
                "security-related software flaws, misconfigurations, product "
                "names, and impact metrics."),
            RWidget('images/resources/mitreattack.png',
                'https://attack.mitre.org',
                'MITRE ATT&CK',
                "MITRE ATT&CK® is a globally-accessible knowledge base of "
                "adversary tactics and techniques based on real-world "
                "observations. The ATT&CK knowledge base is used as a "
                "foundation for the development of specific threat models "
                "and methodologies in the private sector, in government, and "
                "in the cybersecurity product and service community.")
            ]

        # Declare list of News Outlets
        tools_list_layout = QVBoxLayout()
        for tool in tools:
            tools_list_layout.addWidget(tool)

        tools_list.setLayout(tools_list_layout)
        scroll.setWidget(tools_list)
        outer_layout.addWidget(scroll)
            
        # Set layout to main window
        self.setLayout(outer_layout)

class OtherAppsTab(QWidget):
    def __init__(self):
        super(OtherAppsTab, self).__init__()

        # Define Layout
        outer_layout = QVBoxLayout()
        scroll = QScrollArea()        

        # Define news list
        apps_list = QWidget()
        
        apps = [
            RWidget('images/resources/bitdefender.png',
                'https://www.bitdefender.com',
                'Bitdefender',
                'Bitdefender provides cybersecurity solutions with leading '
                'security efficacy, performance and ease of use to small and '
                'medium businesses, mid-market enterprises and consumers.'),
            RWidget('images/resources/nordvpn.png',
                'https://nordvpn.com/cybersecurity-site',
                'NordVPN',
                "VPN stands for virtual private network. NordVPN keeps you "
                "private and secure online by hiding your IP address and "
                "routing your internet traffic through an encrypted connection "
                "to a VPN server (instead of your ISP's servers)."),
            RWidget('images/resources/wireshark.png',
                'https://www.wireshark.org',
                'Wireshark',
                "Wireshark is the world’s foremost and widely-used network "
                "protocol analyzer. It lets you see what’s happening on your "
                "network at a microscopic level and is the de facto (and "
                "often de jure) standard across many commercial and "
                "non-profit enterprises, government agencies, and educational "
                "institutions."),
            RWidget('images/resources/vmware.png',
                'https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html',
                'VMware',
                "VMware Workstation is a line of Desktop Hypervisor products "
                "which lets users run virtual machines, containers and "
                "Kubernetes clusters."),
            RWidget('images/resources/1password.png',
                'https://1password.com',
                '1Password',
                "1Password keeps track of password breaches and other "
                "security problems so you can keep your accounts safe. It "
                "checks for weak, compromised, or duplicated passwords and "
                "lets you know which sites are missing two-factor "
                "authentication or using unsecured HTTP."),
            RWidget('images/resources/nortonlifelock.png',
                'https://lifelock.norton.com',
                'LifeLock by Norton',
                "LifeLock offers comprehensive protection against identity "
                "theft by monitoring against easy-to-miss identity threats "
                "(like payday loans or crimes committed in your name) as "
                "well as identity restoration services and $1 million "
                "coverage for lawyers and other experts if identity theft "
                "does occur while you are a member."),
            RWidget('images/resources/nessus.png',
                'https://www.tenable.com/products/nessus/nessus-professional',
                'Nessus Professional by Tenable',
                "With more than 450 pre-built templates, you can quickly "
                "and conveniently scan for vulnerabilities and audit "
                "configuration compliance against CIS benchmarks or other "
                "best practices. Ease of use is a big selling point of Nessus, "
                "with its intuitive navigation system and overall pleasing user "
                "experience."),
            RWidget('images/resources/snort.png',
                'https://www.snort.org',
                'Snort',
                "Snort works by using a set of rules to find packets that "
                "match against malicious network activity and generate "
                "alerts for users. In addition to its applications as a "
                "full-blown network intrusion prevention system, Snort can "
                "also be used as a packet sniffer like tcpdump or as a "
                "packet logger.")
            ]

        # Declare list of News Outlets
        apps_list_layout = QVBoxLayout()
        for app in apps:
            apps_list_layout.addWidget(app)

        apps_list.setLayout(apps_list_layout)
        scroll.setWidget(apps_list)
        outer_layout.addWidget(scroll)
            
        # Set layout to main window
        self.setLayout(outer_layout)