package start;

import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

import org.python.core.PyInstance;
import org.python.util.PythonInterpreter;
import org.python.core.PyObject;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.Date;
import javax.swing.border.TitledBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

// follow the below link
//https://stackoverflow.com/questions/804466/how-do-i-create-executable-java-program
public class TPMS2 extends JFrame {

    PythonInterpreter interpreter = null;

    // Auto panel (Main)
//    JPanel tpmsScreenPanel = new JPanel();
    JPanel autoTPMSScreenPanel = new JPanel();
    JPanel searchTPMSScreenPanel = new JPanel();

    // Layouts for search function (Main Panel)
    JPanel searchPanel = new JPanel();

    // After search the data
    JPanel searchDataPanel = new JPanel();

    JLabel vehName_label_s = new JLabel();

    JLabel vehName_label_a = new JLabel();

    Font tp_font = new Font("Arial", Font.PLAIN, 30);
    Font tpHeader_font = new Font("Arial", Font.PLAIN, 15).deriveFont(Font.BOLD);

    JLabel fl_pressure_label_s = new JLabel(" --- ");
    JLabel fl_temp_label_s = new JLabel(" --- ");
    JLabel fr_pressure_label_s = new JLabel(" --- ");
    JLabel fr_temp_label_s = new JLabel(" --- ");
    JLabel rlo_pressure_label_s = new JLabel(" --- ");
    JLabel rlo_temp_label_s = new JLabel(" --- ");
    JLabel rli_pressure_label_s = new JLabel(" --- ");
    JLabel rli_temp_label_s = new JLabel(" --- ");
    JLabel rri_pressure_label_s = new JLabel(" --- ");
    JLabel rri_temp_label_s = new JLabel(" --- ");
    JLabel rro_pressure_label_s = new JLabel(" --- ");
    JLabel rro_temp_label_s = new JLabel(" --- ");

    JLabel fl_pressure_label_a = new JLabel(" --- ");
    JLabel fl_temp_label_a = new JLabel(" --- ");
    JLabel fr_pressure_label_a = new JLabel(" --- ");
    JLabel fr_temp_label_a = new JLabel(" --- ");
    JLabel rlo_pressure_label_a = new JLabel(" --- ");
    JLabel rlo_temp_label_a = new JLabel(" --- ");
    JLabel rli_pressure_label_a = new JLabel(" --- ");
    JLabel rli_temp_label_a = new JLabel(" --- ");
    JLabel rri_pressure_label_a = new JLabel(" --- ");
    JLabel rri_temp_label_a = new JLabel(" --- ");
    JLabel rro_pressure_label_a = new JLabel(" --- ");
    JLabel rro_temp_label_a = new JLabel(" --- ");

    // Default lay out
    JPanel keyBoardPanel = new JPanel();

    long vehId = 0;
    String numberString = "";

    JTextField jtf = new JTextField();
    JButton b1 = new JButton("1");
    JButton b2 = new JButton("2");
    JButton b3 = new JButton("3");
    JButton b4 = new JButton("4");
    JButton b5 = new JButton("5");
    JButton b6 = new JButton("6");
    JButton b7 = new JButton("7");
    JButton b8 = new JButton("8");
    JButton b9 = new JButton("9");
    JButton bstart = new JButton("Start");
    JButton b0 = new JButton("0");

    JButton bclear = new JButton("Clear");

    Timer timer;

    public static void main(String[] args) {
        //Create and set up the window.
        TPMS tpms = new TPMS();
        tpms.initUI();
    }

    public void initUI() {

        setBackground(Color.BLACK);
        setTitle("Tyre Pressure & Temperature");

        // Create two tabs
        // 1) Auto - update, 2) Search
        // Create Auto-Update tab
//        tpmsScreenPanel.setLayout(new BorderLayout());
        // Create Search tab
        searchPanel.setLayout(new BorderLayout());
        searchPanel.add(keyBoardPanel);

        desingStaticAutoTPScreen(autoTPMSScreenPanel);
        desingStaticSearchTPScreen(searchTPMSScreenPanel);

        // Add two tabs
        JTabbedPane tp = new JTabbedPane();
        tp.add("Automatic", autoTPMSScreenPanel);
        tp.add("Search", searchPanel);

        tp.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                System.out.println("Tab: " + tp.getSelectedIndex());
                System.out.println("timer running status : " + timer.isRunning());
                if (tp.getSelectedIndex() == 1) {
                    // Search
                    if (null != timer && timer.isRunning()) {
                        timer.stop();
                    }
                    // Visible the keyboard panel
                    numberString = "";
                    jtf.setText("");
                    keyBoardPanel.setVisible(true);
                } else {
                    // Auto
                    if (!timer.isRunning()) {
                        timer.start();
                    }
                    keyBoardPanel.setVisible(false);
                }
            }
        });

        // Add the tabs to screen
        getContentPane().add(tp);

        // Design keyboard panel
        desingKeyboardPanel();

        // Desing search screen after get the Temp & Pressure data
        desingSearchTPStaticScreen();

        // Refresh the screen
        refreshTPScreen();

        // Adding to JFrame
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setUndecorated(true);
        setVisible(true);
        pack();
    }

    public void refreshTPScreen() {
        timer = new Timer(0, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                updateTheTPLiveData();
            }
        });
        timer.setRepeats(true);
        // 10 sec once
        timer.setDelay(10 * 1000);
        timer.start();
    }

    public void findAndUpdateTheSearchVehData() {
        System.out.println("createSearchScreen " + jtf.getText());
        Connection conn = connectToSQLite();
        if (null != jtf.getText() && jtf.getText().trim().length() >= 4) {
            try {
                Statement stmt = conn.createStatement();
                String sql = "SELECT * FROM DeviceDetails where vehName like '%" + jtf.getText() + "%'";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    String rfuid = rs.getString("RFUID");
                    String btuid = rs.getString("BUID");
                    if (null != rfuid && rfuid.trim().length() > 0 && null != btuid && btuid.trim().length() > 0) {
                        // Call the python program
                        TPMS2 ie = new TPMS2();
                        ie.execfile("hello.py");
                        String result = ie.getTPMSDetials(rfuid);
                        JOptionPane.showMessageDialog(searchPanel, "Body message " + result, "Warning", JOptionPane.PLAIN_MESSAGE);
                        keyBoardPanel.setVisible(false);
                        searchDataPanel.add(searchTPMSScreenPanel);
                        searchDataPanel.setVisible(true);
                        vehId = rs.getLong("vehId");
                        searchPanel.add(searchDataPanel);
                        if (!timer.isRunning()) {
                            timer.start();
                        }

                        //updateTheTPLiveData();
                    }
                } else {
                    System.out.println("Vehicle not found with " + jtf.getText());
                    vehId = 0;
                    JOptionPane.showMessageDialog(searchPanel, "Vehicle not found", "Warning", JOptionPane.PLAIN_MESSAGE);
                }
            } catch (Exception e) {
                vehId = 0;
                e.printStackTrace();
            } finally {
                try {
                    if (conn != null) {
                        conn.close();
                    }
                } catch (Exception exp1) {
                    exp1.printStackTrace();
                }
            }
        } else {
            vehId = 0;
            JOptionPane.showMessageDialog(searchPanel, "Please enter 4 digit vehicle number", "Warning", JOptionPane.PLAIN_MESSAGE);
        }
    }

    public void updateTheTPLiveData() {
        System.out.println("start.TPMS.updateTheTPLiveData() " + vehId + " " + new Date());
        Connection conn = connectToSQLite();
        try {
            Statement stmt = conn.createStatement();
            long local_vehId = 0;
            if (vehId != 0) {
                // Search vehicle data only
                local_vehId = vehId;
            } else {
                // Automatic data (Latest)
                String sql = "SELECT vehId FROM Latest_data where count <= 5 order by device_date_time DESC limit 1;";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    local_vehId = rs.getLong("vehId");
                }
            }
            System.out.println("veh id " + local_vehId);
            String sql = "SELECT * FROM Latest_data where vehId = " + local_vehId;
            ResultSet rs1 = stmt.executeQuery(sql);
            while (rs1.next()) {
                try {
                    if (rs1.getString("location").equalsIgnoreCase("01")
                            || rs1.getString("location").equalsIgnoreCase("FL")) {
                        fl_pressure_label_s.setText(rs1.getString("pressure"));
                        fl_temp_label_s.setText(rs1.getString("temp"));
                        fl_pressure_label_a.setText(rs1.getString("pressure"));
                        fl_temp_label_a.setText(rs1.getString("temp"));
                    } else if (rs1.getString("location").equalsIgnoreCase("02")
                            || rs1.getString("location").equalsIgnoreCase("FR")) {
                        fr_pressure_label_s.setText(rs1.getString("pressure"));
                        fr_temp_label_s.setText(rs1.getString("temp"));
                        fr_pressure_label_a.setText(rs1.getString("pressure"));
                        fr_temp_label_a.setText(rs1.getString("temp"));
                    } else if (rs1.getString("location").equalsIgnoreCase("03")
                            || rs1.getString("location").equalsIgnoreCase("RLO")) {
                        rlo_pressure_label_s.setText(rs1.getString("pressure"));
                        rlo_temp_label_s.setText(rs1.getString("temp"));
                        rlo_pressure_label_a.setText(rs1.getString("pressure"));
                        rlo_temp_label_a.setText(rs1.getString("temp"));
                    } else if (rs1.getString("location").equalsIgnoreCase("04")
                            || rs1.getString("location").equalsIgnoreCase("RLI")) {
                        rli_pressure_label_s.setText(rs1.getString("pressure"));
                        rli_temp_label_s.setText(rs1.getString("temp"));
                        rli_pressure_label_a.setText(rs1.getString("pressure"));
                        rli_temp_label_a.setText(rs1.getString("temp"));
                    } else if (rs1.getString("location").equalsIgnoreCase("05")
                            || rs1.getString("location").equalsIgnoreCase("RRI")) {
                        rri_pressure_label_s.setText(rs1.getString("pressure"));
                        rri_temp_label_s.setText(rs1.getString("temp"));
                        rri_pressure_label_a.setText(rs1.getString("pressure"));
                        rri_temp_label_a.setText(rs1.getString("temp"));
                    } else if (rs1.getString("location").equalsIgnoreCase("06")
                            || rs1.getString("location").equalsIgnoreCase("RRO")) {
                        rro_pressure_label_s.setText(rs1.getString("pressure"));
                        rro_temp_label_s.setText(rs1.getString("temp"));
                        rro_pressure_label_a.setText(rs1.getString("pressure"));
                        rro_temp_label_a.setText(rs1.getString("temp"));
                    }
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
            sql = "SELECT vehName FROM DeviceDetails where vehId = "+local_vehId;
            ResultSet rs = stmt.executeQuery(sql);
            if (rs.next()) {
                System.out.println("veh Name: "+rs.getString("vehName"));
                vehName_label_a.setText(rs.getString("vehName"));
                vehName_label_s.setText(rs.getString("vehName"));
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (conn != null) {
                    conn.close();
                    System.out.println("Connection closed");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void desingSearchTPStaticScreen() {
        try {
            searchDataPanel.setLayout(new BorderLayout());
            JPanel vehNamePanle = new JPanel(new GridLayout(1, 3));
            vehNamePanle.setBorder(BorderFactory.createLineBorder(Color.black));
            JButton bstop = new JButton("Stop");
            bstop.setFont(new Font("Arial", Font.PLAIN, 40));
//            bstop.setBackground(Color.RED);
            bstop.setForeground(Color.RED);
            vehNamePanle.add(bstop);

            // Stop button action listerner
            bstop.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    timer.stop();
                    vehId = 0;
                    numberString = "";
                    jtf.setText("");
                    searchDataPanel.setVisible(false);
                    keyBoardPanel.setVisible(true);
                }
            });
            vehName_label_s.setHorizontalAlignment(SwingConstants.CENTER);
            vehName_label_s.setFont(new Font("Arial", Font.PLAIN, 40));

            vehNamePanle.add(vehName_label_s);

            JLabel dateTime_label = new JLabel();
            dateTime_label.setHorizontalAlignment(SwingConstants.RIGHT);
            dateTime_label.setFont(new Font("Arial", Font.PLAIN, 20));

            vehNamePanle.add(dateTime_label);

            bstop.setPreferredSize(new Dimension(200, 100));
            searchDataPanel.add(vehNamePanle, BorderLayout.NORTH);

//            searchDataPanel.add(tpmsScreenPanel, BorderLayout.CENTER);
//            searchPanel.add(searchDataPanel);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void desingKeyboardPanel() {
        try {
            System.out.println("start.TPMS.desingKeyboardPanel() " + new Date());

            keyBoardPanel.setLayout(new BorderLayout());
            // Create key board
            JPanel headerPanel_search = new JPanel(new GridLayout(4, 3));
            b1.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b1);
            b2.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b2);
            b3.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b3);
            b4.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b4);
            b5.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b5);
            b6.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b6);
            b7.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b7);
            b8.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b8);
            b9.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b9);
            bstart.setFont(new Font("Arial", Font.PLAIN, 35));
            headerPanel_search.add(bstart);
            b0.setFont(new Font("Arial", Font.PLAIN, 50));
            headerPanel_search.add(b0);
            bclear.setFont(new Font("Arial", Font.PLAIN, 40));
            headerPanel_search.add(bclear);

            ButtonListener listener = new ButtonListener();

            b0.addActionListener(listener);
            b1.addActionListener(listener);
            b2.addActionListener(listener);
            b3.addActionListener(listener);
            b4.addActionListener(listener);
            b5.addActionListener(listener);
            b6.addActionListener(listener);
            b7.addActionListener(listener);
            b8.addActionListener(listener);
            b9.addActionListener(listener);
            bstart.addActionListener(listener);
            bclear.addActionListener(listener);

            jtf.setHorizontalAlignment(SwingConstants.CENTER);
            jtf.setPreferredSize(new Dimension(200, 150));
            jtf.setFont(new Font("Arial", Font.PLAIN, 50));
            keyBoardPanel.add(jtf, BorderLayout.NORTH);
            keyBoardPanel.add(headerPanel_search, BorderLayout.CENTER);

        } catch (Exception e) {
            e.printStackTrace();

        }
    }

    class ButtonListener implements ActionListener {

        @Override
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == b1) {
                numberString += "1";
            } else if (e.getSource() == b2) {
                numberString += "2";
            } else if (e.getSource() == b3) {
                numberString += "3";
            } else if (e.getSource() == b4) {
                numberString += "4";
            } else if (e.getSource() == b5) {
                numberString += "5";
            } else if (e.getSource() == b6) {
                numberString += "6";
            } else if (e.getSource() == b7) {
                numberString += "7";
            } else if (e.getSource() == b8) {
                numberString += "8";
            } else if (e.getSource() == b9) {
                numberString += "9";
            } else if (e.getSource() == b0) {
                numberString += "0";
            } else if (e.getSource() == bclear) {
                numberString = "";
            } else if (e.getSource() == bstart) {
                findAndUpdateTheSearchVehData();
            }
            jtf.setText(numberString);
        }
    }

// Temp & Pressure static layout
    public void desingStaticAutoTPScreen(JPanel tpmsScreenPanel) {
//        JPanel tpmsScreenPanel = new JPanel();
        tpmsScreenPanel.setLayout(new BorderLayout());
        try {
            vehName_label_a.setPreferredSize(new Dimension(200, 70));
            vehName_label_a.setHorizontalAlignment(SwingConstants.CENTER);

            vehName_label_a.setFont(
                    new Font("Arial", Font.PLAIN, 40));
            tpmsScreenPanel.add(vehName_label_a, BorderLayout.NORTH);

            JPanel bottomMainPanel = new JPanel(new GridLayout(1, 3));

            // For gaps between Temp & Pressure
            GridLayout sizeLayout = new GridLayout(2, 2, 10, 10);

            tpmsScreenPanel.add(bottomMainPanel, BorderLayout.CENTER);
            try {
                // Left side values
                JPanel leftPanel = new JPanel();
                BoxLayout leftLayout = new BoxLayout(leftPanel, BoxLayout.Y_AXIS);
                leftPanel.setLayout(leftLayout);

                JPanel panel11 = new JPanel();
                panel11.setBorder(BorderFactory.createTitledBorder(null, "Front Left", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                fl_pressure_label_a.setFont(tp_font);
                fl_temp_label_a.setFont(tp_font);
                JPanel fl_panel = new JPanel(sizeLayout);
                fl_panel.add(getPressureLabel());
                fl_panel.add(fl_pressure_label_a);
                fl_panel.add(getTempLabel());
                fl_panel.add(fl_temp_label_a);

                panel11.add(fl_panel);

                leftPanel.add(panel11);

                JPanel panel12 = new JPanel();
                panel12.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rlo_pressure_label_a.setFont(tp_font);
                rlo_temp_label_a.setFont(tp_font);
                JPanel rlo_panel = new JPanel(sizeLayout);
                rlo_panel.add(getPressureLabel());
                rlo_panel.add(rlo_pressure_label_a);
                rlo_panel.add(getTempLabel());
                rlo_panel.add(rlo_temp_label_a);

                panel12.add(rlo_panel);

                leftPanel.add(panel12);

                JPanel panel13 = new JPanel();
                panel13.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rli_pressure_label_a.setFont(tp_font);
                rli_temp_label_a.setFont(tp_font);
                JPanel rli_panel = new JPanel(sizeLayout);
                rli_panel.add(getPressureLabel());
                rli_panel.add(rli_pressure_label_a);
                rli_panel.add(getTempLabel());
                rli_panel.add(rli_temp_label_a);

                panel13.add(rli_panel);

                leftPanel.add(panel13);

                leftPanel.setMaximumSize(leftPanel.getPreferredSize());
                leftPanel.setMinimumSize(leftPanel.getPreferredSize());

                // Center - bus image
                JPanel centralPanel = new JPanel();
                try {
                    JLabel imgLabel = new JLabel();
                    BufferedImage img = ImageIO.read(new File("bustyres.png"));
                    Image bimg = img.getScaledInstance(250, 600, Image.SCALE_SMOOTH);
                    ImageIcon imageIcon = new ImageIcon(bimg);
                    imgLabel = new JLabel("", imageIcon, JLabel.CENTER);

                    centralPanel.add(imgLabel);
                } catch (Exception e) {
                    e.printStackTrace();
                }

                // Right side values
                JPanel rightPanel = new JPanel();
                BoxLayout rightLayout = new BoxLayout(rightPanel, BoxLayout.Y_AXIS);
                rightPanel.setLayout(rightLayout);

                JPanel panelFR = new JPanel();
                panelFR.setBorder(BorderFactory.createTitledBorder(null, "Front Right", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                fr_pressure_label_a.setFont(tp_font);
                fr_temp_label_a.setFont(tp_font);
                JPanel fr_panel = new JPanel(sizeLayout);
                fr_panel.add(getPressureLabel());
                fr_panel.add(fr_pressure_label_a);
                fr_panel.add(getTempLabel());
                fr_panel.add(fr_temp_label_a);

                panelFR.add(fr_panel);

                rightPanel.add(panelFR);

                JPanel panelRRO = new JPanel();
                panelRRO.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rro_pressure_label_a.setFont(tp_font);
                rro_temp_label_a.setFont(tp_font);
                JPanel rro_panel = new JPanel(sizeLayout);
                rro_panel.add(getPressureLabel());
                rro_panel.add(rro_pressure_label_a);
                rro_panel.add(getTempLabel());
                rro_panel.add(rro_temp_label_a);

                panelRRO.add(rro_panel);

                rightPanel.add(panelRRO);

                JPanel panelRRI = new JPanel();
                panelRRI.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rri_pressure_label_a.setFont(tp_font);
                rri_temp_label_a.setFont(tp_font);
                JPanel rri_panel = new JPanel(sizeLayout);
                rri_panel.add(getPressureLabel());
                rri_panel.add(rri_pressure_label_a);
                rri_panel.add(getTempLabel());
                rri_panel.add(rri_temp_label_a);

                panelRRI.add(rri_panel);

                rightPanel.add(panelRRI);

                bottomMainPanel.add(leftPanel);
                bottomMainPanel.add(centralPanel);
                bottomMainPanel.add(rightPanel);
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void desingStaticSearchTPScreen(JPanel tpmsScreenPanel) {
//        JPanel tpmsScreenPanel = new JPanel();
        tpmsScreenPanel.setLayout(new BorderLayout());
        try {
            vehName_label_s.setPreferredSize(
                    new Dimension(200, 70));
            vehName_label_s.setHorizontalAlignment(SwingConstants.CENTER);

            vehName_label_s.setFont(
                    new Font("Arial", Font.PLAIN, 40));
            tpmsScreenPanel.add(vehName_label_s, BorderLayout.NORTH);

            JPanel bottomMainPanel = new JPanel(new GridLayout(1, 3));

            // For gaps between Temp & Pressure
            GridLayout sizeLayout = new GridLayout(2, 2, 10, 10);

            tpmsScreenPanel.add(bottomMainPanel, BorderLayout.CENTER);
            try {
                // Left side values
                JPanel leftPanel = new JPanel();
                BoxLayout leftLayout = new BoxLayout(leftPanel, BoxLayout.Y_AXIS);
                leftPanel.setLayout(leftLayout);

                JPanel panel11 = new JPanel();
                panel11.setBorder(BorderFactory.createTitledBorder(null, "Front Left", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                fl_pressure_label_s.setFont(tp_font);
                fl_temp_label_s.setFont(tp_font);
                JPanel fl_panel = new JPanel(sizeLayout);
                fl_panel.add(getPressureLabel());
                fl_panel.add(fl_pressure_label_s);
                fl_panel.add(getTempLabel());
                fl_panel.add(fl_temp_label_s);

                panel11.add(fl_panel);

                leftPanel.add(panel11);

                JPanel panel12 = new JPanel();
                panel12.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rlo_pressure_label_s.setFont(tp_font);
                rlo_temp_label_s.setFont(tp_font);
                JPanel rlo_panel = new JPanel(sizeLayout);
                rlo_panel.add(getPressureLabel());
                rlo_panel.add(rlo_pressure_label_s);
                rlo_panel.add(getTempLabel());
                rlo_panel.add(rlo_temp_label_s);

                panel12.add(rlo_panel);

                leftPanel.add(panel12);

                JPanel panel13 = new JPanel();
                panel13.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rli_pressure_label_s.setFont(tp_font);
                rli_temp_label_s.setFont(tp_font);
                JPanel rli_panel = new JPanel(sizeLayout);
                rli_panel.add(getPressureLabel());
                rli_panel.add(rli_pressure_label_s);
                rli_panel.add(getTempLabel());
                rli_panel.add(rli_temp_label_s);

                panel13.add(rli_panel);

                leftPanel.add(panel13);

                leftPanel.setMaximumSize(leftPanel.getPreferredSize());
                leftPanel.setMinimumSize(leftPanel.getPreferredSize());

                // Center - bus image
                JPanel centralPanel = new JPanel();
                try {
                    JLabel imgLabel = new JLabel();
                    BufferedImage img = ImageIO.read(new File("bustyres.png"));
                    Image bimg = img.getScaledInstance(250, 600, Image.SCALE_SMOOTH);
                    ImageIcon imageIcon = new ImageIcon(bimg);
                    imgLabel = new JLabel("", imageIcon, JLabel.CENTER);

                    centralPanel.add(imgLabel);
                } catch (Exception e) {
                    e.printStackTrace();
                }

                // Right side values
                JPanel rightPanel = new JPanel();
                BoxLayout rightLayout = new BoxLayout(rightPanel, BoxLayout.Y_AXIS);
                rightPanel.setLayout(rightLayout);

                JPanel panelFR = new JPanel();
                panelFR.setBorder(BorderFactory.createTitledBorder(null, "Front Right", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                fr_pressure_label_s.setFont(tp_font);
                fr_temp_label_s.setFont(tp_font);
                JPanel fr_panel = new JPanel(sizeLayout);
                fr_panel.add(getPressureLabel());
                fr_panel.add(fr_pressure_label_s);
                fr_panel.add(getTempLabel());
                fr_panel.add(fr_temp_label_s);

                panelFR.add(fr_panel);

                rightPanel.add(panelFR);

                JPanel panelRRO = new JPanel();
                panelRRO.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rro_pressure_label_s.setFont(tp_font);
                rro_temp_label_s.setFont(tp_font);
                JPanel rro_panel = new JPanel(sizeLayout);
                rro_panel.add(getPressureLabel());
                rro_panel.add(rro_pressure_label_s);
                rro_panel.add(getTempLabel());
                rro_panel.add(rro_temp_label_s);

                panelRRO.add(rro_panel);

                rightPanel.add(panelRRO);

                JPanel panelRRI = new JPanel();
                panelRRI.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rri_pressure_label_s.setFont(tp_font);
                rri_temp_label_s.setFont(tp_font);
                JPanel rri_panel = new JPanel(sizeLayout);
                rri_panel.add(getPressureLabel());
                rri_panel.add(rri_pressure_label_s);
                rri_panel.add(getTempLabel());
                rri_panel.add(rri_temp_label_s);

                panelRRI.add(rri_panel);

                rightPanel.add(panelRRI);

                bottomMainPanel.add(leftPanel);
                bottomMainPanel.add(centralPanel);
                bottomMainPanel.add(rightPanel);
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static JLabel getPressureLabel() {

        JLabel pressure_label = new JLabel("Pressure");
        try {
            BufferedImage pressure_img = ImageIO.read(new File("pressure.png"));
            Image pressure_bimg = pressure_img.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
            ImageIcon pressure_icon = new ImageIcon(pressure_bimg);
            pressure_label = new JLabel("", pressure_icon, JLabel.LEFT);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return pressure_label;
    }

    private static JLabel getTempLabel() {

        JLabel label = new JLabel("Temperature");
        try {
            BufferedImage temp_img = ImageIO.read(new File("temp.png"));
            Image temp_bimg = temp_img.getScaledInstance(70, 80, Image.SCALE_SMOOTH);
            ImageIcon temp_icon = new ImageIcon(temp_bimg);
            label = new JLabel("", temp_icon, JLabel.LEFT);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return label;
    }

    private Connection connectToSQLite() {
        Connection conn = null;
        try {
            // db parameters
            Class.forName("org.sqlite.JDBC");
            String url = "jdbc:sqlite:/opt/JavaServices/sqlite/TPMS.db";
            // create a connection to the database
            conn = DriverManager.getConnection(url);
            System.out.println("Connection to SQLite has been established.");
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println(e.getMessage());
        }
        return conn;
    }

    public TPMS2() {
        PythonInterpreter.initialize(System.getProperties(),
                System.getProperties(), new String[0]);
        this.interpreter = new PythonInterpreter();
    }

    void execfile(final String fileName) {
        this.interpreter.execfile(fileName);
    }

    public String getTPMSDetials(String rfid) {

        PyObject str = this.interpreter.eval("repr(run('" + rfid + "'))");
        return str.toString();
    }

    PyInstance createClass(final String className, final String opts) {
        return (PyInstance) this.interpreter.eval(className + "(" + opts + ")");
    }
}
